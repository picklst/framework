FROM python:3-alpine as base

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libxml2-dev libxslt-dev


FROM base as framework

ADD . /framework
WORKDIR /framework

RUN pip install -r requirements.txt


FROM framework as production

RUN pip install --upgrade pip gunicorn