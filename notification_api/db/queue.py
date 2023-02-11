from functools import lru_cache

from fastapi import Depends
import pika
from storage.queue import QueueService


rabbitmq: pika.BlockingConnection | None = None


async def get_rabbitmq():
    return rabbitmq

@lru_cache()
def get_queue_service(
    rabbitmq: pika.BlockingConnection = Depends(get_rabbitmq),
) -> QueueService:
    return QueueService(rabbitmq)