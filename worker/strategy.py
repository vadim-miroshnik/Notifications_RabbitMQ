from abc import ABCMeta, abstractmethod


class Message:
    subject: str
    body: str
    data = {}

    def __init__(self, subject: str, body: str, **kwargs):
        self.subject = subject
        self.body = body
        self.data = kwargs

    def send(self, transport):
        transport(self.subject, self.body, **self.data)


class ITransport(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self):
        pass


class Email(ITransport):

    def send(self, subject: str, body: str, **kwargs):
        print(f"Email")

    __call__ = send


class Websocket(ITransport):

    def push(self, subject: str, body: str, **kwargs):
        print(f"Websocket")

    __call__ = push


class SMS(ITransport):

    def send(self, subject: str, body: str, **kwargs):
        print(f"SMS")

    __call__ = send


if __name__ == "__main__":
    message = Message("test", "test", recepients=["test", "test"], phone="123456")
    message.send(Email())
    message.send(Websocket())
    message.send(SMS())