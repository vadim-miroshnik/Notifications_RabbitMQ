FROM python:3.10.8

RUN apt update \
    && apt install -y netcat \
    && apt autoclean

WORKDIR /opt/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

RUN chmod +x init.sh

CMD ["./init.sh"]