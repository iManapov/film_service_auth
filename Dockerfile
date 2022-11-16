FROM python:3.10.6-slim

EXPOSE 5001

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  apt-get update \
     && apt-get install -y gcc \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .
COPY src/core/docker.env src/core/.env
COPY tests/functional/docker.env tests/functional/.env

ENTRYPOINT ["bash", "entrypoint.sh"]

