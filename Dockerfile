FROM python:3.10-slim

ARG OPENSSL_CONF=/root/openssl.cnf

COPY requirements*.txt /tmp/
ADD sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends vim iputils-ping \
net-tools netcat-traditional curl g++ unixodbc unixodbc-dev

RUN pip3 install -r /tmp/requirements.txt \
&& pip3 install SQLAlchemy==1.4.46 --no-deps

WORKDIR /mailing
ADD ./src ./
