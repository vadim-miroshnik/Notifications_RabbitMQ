import asyncio
from email.message import EmailMessage

import aio_pika
import aiosmtplib
import orjson
from config import settings
from jinja2 import Environment
from models import Notification, NotifTypeEnum, PriorityEnum
from pydantic import parse_obj_as


async def send_email(email: EmailMessage):
    await aiosmtplib.send(
        email,
        hostname=settings.worker.smtp_server,
        port=settings.worker.smtp_port,
        username=settings.worker.smtp_user,
        password=settings.worker.smtp_password,
        use_tls=True
    )


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():
        message_body = parse_obj_as(Notification, orjson.loads(message.body))
        if message_body.notif_type == NotifTypeEnum.EMAIL:
            for recipient in message_body.recipients:
                email = EmailMessage()
                email["From"] = settings.worker.smtp_user
                email["To"] = recipient.email
                email["Subject"] = message_body.subject
                env = Environment()
                template = env.from_string(message_body.template)
                output = template.render(recipient.data)
                email.set_content(output)
                await send_email(email)


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
