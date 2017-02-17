SHELL=/bin/bash
ifndef ELASTIC_VERSION
export ELASTIC_VERSION := $(shell cat version.txt)
endif

ifdef STAGING_BUILD_NUM
export VERSION_TAG := $(ELASTIC_VERSION)-$(STAGING_BUILD_NUM)
DOWNLOAD_URL_ROOT := https://staging.elastic.co/downloads/beats
else
export VERSION_TAG := $(ELASTIC_VERSION)
DOWNLOAD_URL_ROOT := https://artifacts.elastic.co/downloads/beats
endif

BEATS := $(shell cat beats.txt)
REGISTRY := docker.elastic.co

# Make sure we run local versions of everything, particularly commands
# installed into our virtualenv with pip eg. `docker-compose`.
export PATH := ./bin:./venv/bin:$(PATH)

# A little helper for running curl against the Elasticsearch container.
# We'll use the Kibana container, since we know it has network access to
# Elasticsearch.
ES_URL := http://elastic:changeme@elasticsearch:9200
ES_GET := docker-compose run --rm kibana curl -XGET $(ES_URL)
ES_PUT := docker-compose run --rm kibana curl -XPUT $(ES_URL)


# Run the tests with testinfra (actually our custom wrapper at ./bin/testinfra)
# REF: http://testinfra.readthedocs.io/en/latest/
test: all
	testinfra -v test/
.PHONY: test

all: venv images docker-compose.yml

docker-compose.yml: templates/docker-compose.yml.j2
	jinja2 \
	  -D beats='$(BEATS)' \
	  -D version=$(VERSION_TAG) \
	  -D registry=$(REGISTRY) \
	  templates/docker-compose.yml.j2 > docker-compose.yml

# Bring up a full-stack demo with Elasticsearch, Kibana and all the Unix Beats.
# Point a browser at http://localhost:5601 to see the results, and log in to
# to Kibana with "elastic"/"changeme".
demo: all
	docker-compose up -d elasticsearch
	until $(ES_GET); do sleep 1; done
	make import-dashboards
	docker-compose up

# Build images for all the Beats, generate the Dockerfiles as we go.
images: $(BEATS)
$(BEATS):
	mkdir -p build/$@/config
	touch build/$@/config/$@.yml
	jinja2 \
	  -D beat=$@ \
	  -D version=$(ELASTIC_VERSION) \
	  -D url=$(DOWNLOAD_URL_ROOT)/$@/$@-$(VERSION_TAG)-linux-x86_64.tar.gz \
          templates/Dockerfile.j2 > build/$@/Dockerfile
	docker build --tag=$(REGISTRY)/beats/$@:$(VERSION_TAG) build/$@

# Have each Beat install its default dashboards in Elasticsearch. Also set
# Kibana's default index pattern as a convenience for `make demo`.
import-dashboards: all
	for beat in $(BEATS); do \
	  docker-compose run --rm $$beat \
	    scripts/import_dashboards \
	    -file beats-dashboards-$(ELASTIC_VERSION).zip \
	    -es http://elasticsearch:9200 \
	    -user elastic \
	    -pass changeme ;\
	done
	$(ES_PUT)/.kibana/config/$(ELASTIC_VERSION) -d '{"defaultIndex" : "metricbeat-*"}'

venv: requirements.txt
	test -d venv || virtualenv --python=python3.5 venv
	pip install -r requirements.txt
	touch venv

clean: venv
	docker-compose down -v || true
	rm -f docker-compose.yml build/*/Dockerfile
	rm -rf venv
	find . -name __pycache__ | xargs rm -rf
