FROM python:3
MAINTAINER Andre Kohn <andre@kohn.io>

# Install mysqldb
RUN apt-get update && \
	apt-get install -y mysql-client && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

# Install application requirements
COPY requirements.txt /srv/mc/requirements.txt
RUN pip install -r /srv/mc/requirements.txt

# Add application folder and pip requirements
COPY mendeleycache /srv/mc/mendeleycache

# Add application to pythonpath
ENV PYTHONPATH $PYTHONPATH:/srv/mc/

# Add pipeline script
COPY docker/pipeline.sh /usr/local/bin/pipeline
RUN chmod +x /usr/local/bin/pipeline

# Expose 8080 as default gunicorn port
EXPOSE 8080

# Adding entrypoint script
COPY docker/entrypoint.sh /srv/mc/entrypoint.sh
RUN chmod +x /srv/mc/entrypoint.sh

ENTRYPOINT ["/srv/mc/entrypoint.sh"]
CMD ["gunicorn", "-b 0.0.0.0:8080", "-w 4", "mendeleycache.app:app"]
