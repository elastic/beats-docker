FROM ubuntu:16.04
MAINTAINER Elastic Docker Team <docker@elastic.co>

ARG ELASTIC_VERSION
ARG DOWNLOAD_URL

RUN apt-get update && apt-get install -y curl && apt-get clean

RUN curl -Lso - ${DOWNLOAD_URL} | \
    tar zxf - -C /usr/share && \
    mv /usr/share/metricbeat-5.2.0-linux-x86_64 /usr/share/metricbeat
ENV PATH=/usr/share/metricbeat:$PATH

COPY config/metricbeat.yml /usr/share/metricbeat/

# Provide a non-root user to run the process.
RUN chown --recursive 1000:1000 /usr/share/metricbeat && \
    addgroup --gid 1000 metricbeat && \
    adduser --disabled-password --gecos=metricbeat --uid=1000 --gid=1000 --home /usr/share/metricbeat metricbeat
USER metricbeat
WORKDIR /usr/share/metricbeat

CMD ["metricbeat", "-e", "-v"]
