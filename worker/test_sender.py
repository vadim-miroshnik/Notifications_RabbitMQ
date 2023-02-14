import asyncio
import aio_pika
from config import settings
import orjson
from models import Notification, NotifTypeEnum


async def main() -> None:
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq.server,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.user,
        password=settings.rabbitmq.password,
    )
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(name="Ex")
        msg = Notification(notif_type=NotifTypeEnum.EMAIL,
                           subject="subj",
                           template="{{ title }} {{ text }}",
                           content_data=[{"title": "Hello", "text": "test"}, ],
                           recepients=["aka.fall3n@gmail.com"])
        await exchange.publish(message=aio_pika.Message(body=orjson.dumps(msg.dict())), routing_key="messages")


if __name__ == "__main__":
    asyncio.run(main())
