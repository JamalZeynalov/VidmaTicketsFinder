FROM python:3.11.0

MAINTAINER jamalzeynalov@compstak.com

COPY . /tmp
WORKDIR /tmp

RUN pip install -r requirements.txt

ENTRYPOINT python vidma.py -u
