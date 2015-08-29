FROM python:3.4
MAINTAINER Andre Kohn <andre@kohn.io>

COPY mendeleycache /srv/app/mendeleycache
COPY requirements.txt /tmp/requirements.txt
COPY config.yml /srv/app/config.yml

RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ENV PYTHONPATH $PYTHONPATH:/srv

EXPOSE 8080

CMD ["gunicorn", "-b 0.0.0.0:8080", "-w 4", "mendeleycache.app:app"]
