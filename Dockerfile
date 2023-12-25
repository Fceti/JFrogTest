FROM python:3.9.13-alpine3.16

MAINTAINER Pavel Voskoboinikov  <Pavel.Voskoboinikov@enterra-inc.com>

ARG env_jenkins

RUN  mkdir /APP &&\
     python --version && pip --version &&\
     pip install --upgrade pip &&\
     pip install --upgrade setuptools &&\
     pip install click CloudFlare

COPY ./cloudflare.py /APP

WORKDIR /APP

ENTRYPOINT python /APP/cloudflare.py -j "$ENV_JENKINS"

