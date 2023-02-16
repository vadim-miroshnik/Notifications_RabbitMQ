import asyncio
import smtplib
import ssl
from email.message import EmailMessage

import aio_pika
import orjson
from jinja2 import Environment
from pydantic import parse_obj_as

from config import settings
from models import Notification, PriorityEnum, NotifTypeEnum


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():
        message_body = parse_obj_as(Notification, orjson.loads(message.body))
        if message_body.notif_type == NotifTypeEnum.EMAIL:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(settings.worker.smtp_server, settings.worker.smtp_port, context=context) as server:
                server.login(settings.worker.smtp_user, settings.worker.smtp_password)
                for recipient in message_body.recipients:
                    email = EmailMessage()
                    email["From"] = settings.worker.smtp_user
                    email["To"] = recipient.email
                    email["Subject"] = message_body.subject
                    env = Environment()
                    template = env.from_string(message_body.template)
                    output = template.render(recipient.data)
                    email.set_content(output)
                    server.sendmail(email["From"], email["To"], email.as_string())


async def main() -> None:
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq.server,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.user,
        password=settings.rabbitmq.password,
    )
    channel = await connection.channel()
    exchange = await channel.declare_exchange(name="notifications")
    queues = {}
    for priority in PriorityEnum:
        queues[priority] = await channel.declare_queue(priority, durable=True)
        await queues[priority].bind(exchange=exchange.name)
        await queues[priority].consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
