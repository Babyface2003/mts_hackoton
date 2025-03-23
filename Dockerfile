FROM python:3.12-alpine

WORKDIR /app

COPY ../mtd1 /app

ENTRYPOINT python main.py

