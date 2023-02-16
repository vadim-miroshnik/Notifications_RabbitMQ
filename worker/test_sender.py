import asyncio
import aio_pika
from config import settings
import orjson
from models import Notification, NotifTypeEnum, PriorityEnum, Recipient


async def main() -> None:
    connection = await aio_pika.connect_robust(
        host=settings.rabbitmq.server,
        port=settings.rabbitmq.port,
        login=settings.rabbitmq.user,
        password=settings.rabbitmq.password,
    )
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(name="notifications")
        msg = Notification(id="",
                           notif_type=NotifTypeEnum.EMAIL,
                           subject="subj",
                           template="{{ title }} {{ text }}",
                           recipients=[Recipient(email="aka.fall3n@gmail.com", data={"title": "Hello Vadim", "text": "test"}),
                                       Recipient(email="aka.fall4n@gmail.com", data={"title": "Hello Maxim", "text": "test"})],
                           priority=PriorityEnum.HIGH)
        queue = await channel.declare_queue(msg.priority, durable=True)
        await queue.bind(exchange=exchange.name)
        await exchange.publish(message=aio_pika.Message(body=orjson.dumps(msg.dict())), routing_key=queue.name)


if __name__ == "__main__":
    asyncio.run(main())
