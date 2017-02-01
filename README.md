## Description

This repository contains the official [Beats][beats] Docker images from
[Elastic][elastic].

[beats]: https://www.elastic.co/products/beats
[elastic]: https://www.elastic.co/

## Supported Docker versions

The images have been tested on Docker 1.13.0.

## Contributing, issues and testing

Acceptance tests for the image are located in the `test` directory, and can
be invoked with `make test`. Python 3.5 and virtualenv are required to run
the tests.

This image is built on [Ubuntu 16.04][ubuntu-1604].

[ubuntu-1604]: https://github.com/tianon/docker-brew-ubuntu-core/blob/188bcceb999c0c465b3053efefd4e1a03d3fc47e/xenial/Dockerfile
