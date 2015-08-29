FROM python:3.4
MAINTAINER Andre Kohn <andre@kohn.io>

# Add application folder and pip requirements
COPY mendeleycache /srv/mc/mendeleycache
COPY requirements.txt /srv/mc/requirements.txt

# This is an empty placeholder file to enable sqlite .db's inside docker volumes
COPY main.db /srv/mc/main.db

# Install requirements
RUN pip install -r /srv/mc/requirements.txt

# Add application to pythonpath
ENV PYTHONPATH $PYTHONPATH:/srv/mc/

# Expose 8080 as default gunicorn port
EXPOSE 8080

CMD ["gunicorn", "-b 0.0.0.0:8080", "-w 4", "mendeleycache.app:app"]
