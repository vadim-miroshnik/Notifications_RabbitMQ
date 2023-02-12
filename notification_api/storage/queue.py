#import pika
import aio_pika
from aio_pika.abc import AbstractRobustConnection


class QueueService:
    # def __init__(self, connection: pika.BlockingConnection):
    #    self.connection = connection

    def __init__(self, connection: AbstractRobustConnection):
        self.connection = connection

    async def send(self, topic, key, value):
        channel = await self.connection.channel()
        await channel.default_exchange.publish(aio_pika.Message(body=value.encode()),
                                               routing_key=topic)

    async def read(self, topic):
        channel = await self.connection.channel()
        queue = await channel.declare_queue(topic, auto_delete=True)
        print(queue)
        async with queue.iterator() as iter:
            async for message in iter:
                async with message.process():
                    print(message.body)
