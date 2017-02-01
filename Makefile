SHELL=/bin/bash
ifndef ELASTIC_VERSION
ELASTIC_VERSION=5.2.0
endif

ifdef STAGING_BUILD_NUM
VERSION_TAG=$(ELASTIC_VERSION)-$(STAGING_BUILD_NUM)
DOWNLOAD_URL_ROOT=https://staging.elastic.co/downloads/beats
else
VERSION_TAG=$(ELASTIC_VERSION)
DOWNLOAD_URL_ROOT=https://artifacts.elastic.co/downloads/beats
endif

REGISTRY=docker.elastic.co

export ELASTIC_VERSION
export VERSION_TAG

test: metricbeat
	test -d venv || virtualenv --python=python3.5 venv
	( \
	  source venv/bin/activate; \
	  pip install -r test/requirements.txt; \
	  py.test test/ \
	)

all: metricbeat

metricbeat:
	IMAGE=$(REGISTRY)/beats/metricbeat/metricbeat:$(VERSION_TAG) \
	DOWNLOAD_URL=$(DOWNLOAD_URL_ROOT)/metricbeat/metricbeat-$(VERSION_TAG)-linux-x86_64.tar.gz \
	docker-compose build --pull metricbeat

clean:
	docker-compose down
	docker-compose rm --force

demo:
	IMAGE=$(REGISTRY)/beats/metricbeat/metricbeat:$(VERSION_TAG) \
	DOWNLOAD_URL=$(DOWNLOAD_URL_ROOT)/metricbeat/metricbeat-$(VERSION_TAG)-linux-x86_64.tar.gz \
	docker-compose -f docker-compose.demo.yml up

.PHONY: test all metricbeat clean demo
