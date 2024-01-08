FROM python:3.11-slim-buster

WORKDIR app

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . .
RUN apt-get update && apt-get install -y supervisor
RUN pip3 install -r requirements.txt

CMD ["/usr/bin/supervisord"]