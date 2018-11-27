## Description

This repository contains the official [Beats][beats] Docker images from
[Elastic][elastic].

Documentation can be found on the [Elastic website][elastic]:

* [auditbeat][auditbeat]
* [filebeat][filebeat]
* [heartbeat][heartbeat]
* [journalbeat][journalbeat]
* [metricbeat][metricbeat]
* [packetbeat][packetbeat]

[beats]: https://www.elastic.co/products/beats
[elastic]: https://www.elastic.co/
[auditbeat]: https://www.elastic.co/guide/en/beats/auditbeat/current/running-on-docker.html
[filebeat]: https://www.elastic.co/guide/en/beats/filebeat/current/running-on-docker.html
[heartbeat]: https://www.elastic.co/guide/en/beats/heartbeat/current/running-on-docker.html
[journalbeat]: https://www.elastic.co/guide/en/beats/journalbeat/current/running-on-docker.html
[metricbeat]: https://www.elastic.co/guide/en/beats/metricbeat/current/running-on-docker.html
[packetbeat]: https://www.elastic.co/guide/en/beats/packetbeat/current/running-on-docker.html

## Requirements
A full build and test requires:
* Docker
* GNU Make
* Python 3.5 with Virtualenv

## Supported Docker versions

The images have been tested on Docker 17.03.1-ce

## Running a build
To build images with a released version of Beats, check out the corresponding
branch for the version, and run Make while specifying the exact version desired.
Like this:
```
git checkout 6.3
ELASTIC_VERSION=6.3.1 make
```

To build images with the latest nightly snapshots of Beats, run:
```
make from-snapshot
```

## Contributing, issues and testing

Acceptance tests for the images are located in the `test` directory,
and can be invoked with `make test`. Python 3.5 is required to run the
tests. They are based on the
excellent [testinfra](http://testinfra.readthedocs.io/en/latest/),
which is itself based on
the wonderful [pytest](http://doc.pytest.org/en/latest/).

`beats-docker` is developed under a test-driven
workflow, so please refrain from submitting patches without test
coverage. If you are not familiar with testing in Python, please
raise an issue instead.

The images are built on [CentOS 7][centos-7].

[centos-7]: https://github.com/CentOS/sig-cloud-instance-images/blob/50281d86d6ed5c61975971150adfd0ede86423bb/docker/Dockerfile
