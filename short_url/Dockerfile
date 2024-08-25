FROM python:3.12.4-alpine3.20

RUN apk add --no-cache postgresql-client

WORKDIR /usr/share/app/

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt