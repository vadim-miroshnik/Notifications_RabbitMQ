import smtplib
import ssl
from abc import ABCMeta, abstractmethod
from email.message import EmailMessage
from models import Notification
from config import settings
from jinja2 import Environment


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
    def send(self, message: Notification):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.worker.smtp_server, settings.worker.smtp_port, context=context) as server:
            server.login(settings.worker.smtp_user, settings.worker.smtp_password)
            message = EmailMessage()
            message["From"] = settings.worker.smtp_user
            message["To"] = Notification.recepients
            message["Subject"] = Notification.subject
            env = Environment()
            template = env.from_string(Notification.template)
            output = template.render(Notification.content_data)
            message.set_content(output)
            server.sendmail(message["From"], message["To"], message.as_string())

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
