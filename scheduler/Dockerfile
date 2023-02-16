FROM ubuntu:latest

RUN apt update \
    && apt install -y \
      cron \
      curl \
    && apt autoclean

WORKDIR /opt/app

COPY . .

RUN chmod +x *.sh

CMD ["./init.sh"]