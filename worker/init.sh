#!/bin/bash

while ! nc -z "$RABBITMQ__SERVER" "$RABBITMQ__PORT"
do
  sleep 3
done
echo "+++ Rabbit is ready +++"
python3 main.py