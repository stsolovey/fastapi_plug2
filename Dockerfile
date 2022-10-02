# Dockerfile

# pull the official docker image
FROM python:3.10.4-alpine

# set work directory
WORKDIR /fastapi_plug2

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt && mkdir --parents ~/.postgresql && wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" --output-document ~/.postgresql/root.crt && chmod 0600 ~/.postgresql/root.crt

# copy project
COPY . .