FROM python:3.11-slim-buster

WORKDIR app

ENV TERM xterm
ENV C_FORCE_ROOT true

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .
RUN apt-get update && apt-get install -y supervisor
RUN pip3 install -r requirements.txt

CMD ["/usr/bin/supervisord"]