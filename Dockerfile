FROM python:3.9.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev postgresql-dev libffi-dev make build-base py-pip jpeg-dev zlib-dev
RUN pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /code/
COPY . /code/
RUN chmod +x /code/entrypoint.sh
