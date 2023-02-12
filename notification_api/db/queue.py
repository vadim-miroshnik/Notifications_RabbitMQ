import asyncio
from functools import lru_cache

from fastapi import Depends
#import pika
import aio_pika
from aio_pika.abc import AbstractRobustConnection
from storage.queue import QueueService


#rabbitmq: pika.BlockingConnection | None = None
rabbitmq: AbstractRobustConnection | None = None

# rabbitmq = aio_pika.connect_robust("amqp://guest:guest@localhost:5672")


async def get_rabbitmq():
    global rabbitmq
    while True:
        try:
            rabbitmq = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672", loop=asyncio.get_event_loop())
            break
        except ConnectionError as e:
            print(e)
            await asyncio.sleep(5)
    return rabbitmq

'''
@lru_cache()
def get_queue_service(
    rabbitmq: pika.BlockingConnection = Depends(get_rabbitmq),
) -> QueueService:
    return QueueService(rabbitmq)
'''

@lru_cache()
def get_queue_service(
    rabbit: AbstractRobustConnection = Depends(get_rabbitmq),
) -> QueueService:
    return QueueService(rabbit)
