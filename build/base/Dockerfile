FROM python:3.11-slim

LABEL title "Mazes-for-programmers-Python-src"
LABEL maintainer "Diego / Kartones"
LABEL contrib1 "https://github.com/Kartones"
LABEL url "https://kartones.net"
LABEL twitter "@kartones"

# Define environment vars to expose to container here
# ENV <key> <value>

# Env vars sent from docker-compose or docker build
ARG uid=1000
ARG gid=1000

RUN getent group $gid || groupadd --gid $gid mazes-for-programmers
RUN getent passwd $uid || useradd -m -u $uid -g $gid mazes-for-programmers

RUN chown -R $uid:$gid /usr/local

RUN apt-get clean && apt-get -y update

USER $uid

RUN pip install --upgrade pip

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
