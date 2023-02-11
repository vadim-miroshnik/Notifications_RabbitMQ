import pika


class QueueService:
    def __init__(self, connection: pika.BlockingConnection):
        self.connection = connection

    def send(self, topic, key, value):
        pass