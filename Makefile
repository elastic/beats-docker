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
export PATH := ./bin:./venv/bin:$(PATH)


test: all
	testinfra -v test/

all: venv images compose-file

compose-file:
	jinja2 \
	  -D beats='$(BEATS)' \
	  -D version=$(VERSION_TAG) \
	  -D registry=$(REGISTRY) \
	  templates/docker-compose.yml.j2 > docker-compose.yml

demo: all
	docker-compose up

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

import-dashboards:
	for beat in $(BEATS); do \
	  docker-compose run --rm $$beat \
	    scripts/import_dashboards \
	    -file beats-dashboards-$(ELASTIC_VERSION).zip \
	    -es http://elasticsearch:9200 \
	    -user elastic \
	    -pass changeme ;\
	done

venv:
	test -d venv || virtualenv --python=python3.5 venv
	pip install -r requirements.txt

clean: venv
	docker-compose down -v || true
	rm -f docker-compose.yml build/*/Dockerfile
	rm -rf venv
	find . -name __pycache__ | xargs rm -rf

.PHONY: clean test all demo $(BEATS) venv compose-file
