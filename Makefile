SHELL=/bin/bash
ifndef ELASTIC_VERSION
export ELASTIC_VERSION := $(shell cat version.txt)
endif

ifdef STAGING_BUILD_NUM
export VERSION_TAG := $(ELASTIC_VERSION)-$(STAGING_BUILD_NUM)
DOWNLOAD_URL_ROOT := https://staging.elastic.co/$(VERSION_TAG)/downloads/beats
else
export VERSION_TAG := $(ELASTIC_VERSION)
DOWNLOAD_URL_ROOT := https://artifacts.elastic.co/downloads/beats
endif

BEATS := $(shell cat beats.txt)
REGISTRY := docker.elastic.co

# Make sure we run local versions of everything, particularly commands
# installed into our virtualenv with pip eg. `docker-compose`.
export PATH := ./bin:./venv/bin:$(PATH)

all: venv images docker-compose.yml test

# Run the tests with testinfra (actually our custom wrapper at ./bin/testinfra)
# REF: http://testinfra.readthedocs.io/en/latest/
test: lint all
	testinfra -v test/
.PHONY: test

lint: venv
	flake8 test/

docker-compose.yml: venv
	jinja2 \
	  -D beats='$(BEATS)' \
	  -D version=$(VERSION_TAG) \
	  -D registry=$(REGISTRY) \
	  templates/docker-compose.yml.j2 > docker-compose.yml
.PHONY: docker-compose.yml

# Bring up a full-stack demo with Elasticsearch, Kibana and all the Unix Beats.
# Point a browser at http://localhost:5601 to see the results, and log in to
# to Kibana with "elastic"/"changeme".
demo: all
	docker-compose up

# Build images for all the Beats, generate the Dockerfiles as we go.
images: $(BEATS)
$(BEATS):
	mkdir -p build/$@/config
	touch build/$@/config/$@.yml
	jinja2 \
	  -D beat=$@ \
	  -D version=$(ELASTIC_VERSION) \
	  -D url=$(DOWNLOAD_URL_ROOT)/$@/$@-$(ELASTIC_VERSION)-linux-x86_64.tar.gz \
	  -D dashboards_url=$(DOWNLOAD_URL_ROOT)/beats-dashboards/beats-dashboards-$(ELASTIC_VERSION).zip \
          templates/Dockerfile.j2 > build/$@/Dockerfile
	docker build --tag=$(REGISTRY)/beats/$@:$(VERSION_TAG) build/$@

push: all
	for beat in $(BEATS); do \
	  docker push $(REGISTRY)/beats/$$beat:$(VERSION_TAG); \
	done

venv: requirements.txt
	test -d venv || virtualenv --python=python3.5 venv
	pip install -r requirements.txt
	touch venv

clean: venv
	docker-compose down -v || true
	rm -f docker-compose.yml build/*/Dockerfile build/*/config/*.sh
	rm -rf venv
	find . -name __pycache__ | xargs rm -rf
