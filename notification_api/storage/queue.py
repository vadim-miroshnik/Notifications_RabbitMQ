#import pika
import json
import aio_pika
from aio_pika.abc import AbstractRobustConnection


class QueueService:
    # def __init__(self, connection: pika.BlockingConnection):
    #    self.connection = connection

    def __init__(self, connection: AbstractRobustConnection):
        self.connection = connection

    async def send(self, priority, topic, value):
        # Creating channel
        channel = await self.connection.channel()

        # Declaring exchange
        exchange = await channel.declare_exchange("notifications", auto_delete=True)

        # Declaring queue
        queue = await channel.declare_queue(priority, auto_delete=True)

        # Binding queue
        await queue.bind(exchange, topic)

        await exchange.publish(
            aio_pika.Message(
                str(value.as_dict).encode(),
                content_type="application/json",
            ),
            topic,
        )

'''
    async def read(self, topic):
        channel = await self.connection.channel()
        queue = await channel.declare_queue(topic, auto_delete=True)
        print(queue)
        async with queue.iterator() as iter:
            async for message in iter:
                async with message.process():
                    print(message.body)
'''