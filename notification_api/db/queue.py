import asyncio
from functools import lru_cache

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from fastapi import Depends

from core.config import settings
from storage.queue import QueueService

rabbitmq: AbstractRobustConnection | None = None


async def get_rabbitmq():
    global rabbitmq
    while True:
        try:
            rabbitmq = await aio_pika.connect_robust(
                host=settings.rabbitmq.server,
                port=settings.rabbitmq.port,
                login=settings.rabbitmq.user,
                password=settings.rabbitmq.password,
                loop=asyncio.get_event_loop(),
            )
            break
        except ConnectionError as e:
            await asyncio.sleep(5)
    return rabbitmq


@lru_cache()
def get_queue_service(
    rabbit: AbstractRobustConnection = Depends(get_rabbitmq),
) -> QueueService:
    return QueueService(rabbit)
