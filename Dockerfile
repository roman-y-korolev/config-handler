FROM python:3.6-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev bash

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80