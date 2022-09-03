FROM python:2-alpine as builder

RUN apk add --no-cache --virtual .build-deps build-base mariadb-dev jpeg-dev zlib-dev tiff-dev libwebp-dev

RUN mkdir /install
COPY requirements requirements/
COPY requirements.txt requirements.txt
RUN pip install --install-option="--prefix=/install" -r requirements.txt

FROM python:2-alpine

RUN apk add --no-cache py-mysqldb mariadb-dev
COPY --from=builder /install /usr/local

RUN mkdir /app
WORKDIR /app
COPY . /app

EXPOSE 80 3000