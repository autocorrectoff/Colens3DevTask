FROM python:3.7.4-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get -y dist-upgrade && apt-get -y --no-install-recommends install dumb-init apt-utils  \
	 && pip3 install --no-cache-dir -r /app/requirements.txt && rm -rf /var/lib/apt/lists/* \
	 && rm -rf /root/.cache && apt-get -y clean

COPY docker-entrypoint.sh /



EXPOSE 5000

ENTRYPOINT ["/usr/bin/dumb-init", "sh", "docker-entrypoint.sh"]