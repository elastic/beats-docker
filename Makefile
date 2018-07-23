SHELL=/bin/bash

ifndef ELASTIC_VERSION
export ELASTIC_VERSION := $(shell ./bin/elastic-version)
endif

ifdef STAGING_BUILD_NUM
export VERSION_TAG := $(ELASTIC_VERSION)-$(STAGING_BUILD_NUM)
DOWNLOAD_URL_ROOT ?= https://staging.elastic.co/$(VERSION_TAG)/downloads/beats
else
export VERSION_TAG := $(ELASTIC_VERSION)
DOWNLOAD_URL_ROOT ?= https://artifacts.elastic.co/downloads/beats
endif

BUILD_ARTIFACT_PATH ?= beats/build/distributions

BEATS := $(shell cat beats.txt)
REGISTRY ?= docker.elastic.co
HTTPD ?= beats-docker-artifact-server

IMAGE_FLAVORS ?= oss full
FIGLET := pyfiglet -w 160 -f puffy

# Make sure we run local versions of everything, particularly commands
# installed into our virtualenv with pip eg. `docker-compose`.
export PATH := ./bin:./venv/bin:$(PATH)

all: venv images docker-compose.yml test

# Run the tests with testinfra (actually our custom wrapper at ./bin/testinfra)
# REF: http://testinfra.readthedocs.io/en/latest/
test: lint docker-compose.yml
	$(foreach FLAVOR, $(IMAGE_FLAVORS), \
	  $(FIGLET) "test: $(FLAVOR)"; \
	  ./bin/pytest -v --image-flavor=$(FLAVOR) tests/; \
	)
.PHONY: test

lint: venv
	flake8 tests/

docker-compose.yml: venv
	$(foreach FLAVOR, $(IMAGE_FLAVORS), \
	jinja2 \
	  -D beats='$(BEATS)' \
	  -D version=$(VERSION_TAG) \
	  -D registry=$(REGISTRY) \
	  -D image_flavor='$(FLAVOR)' \
	  templates/docker-compose.yml.j2 > docker-compose-$(FLAVOR).yml; \
	)
.PHONY: docker-compose.yml

# Bring up a full-stack demo with Elasticsearch, Kibana and all the Unix Beats.
# Point a browser at http://localhost:5601 to see the results, and log in to
# to Kibana with "elastic"/"changeme".
demo: all
	docker-compose up

# Build images for all the Beats, generate the Dockerfiles as we go.
images: $(BEATS)
$(BEATS): venv
	mkdir -p build/$@/config
	touch build/$@/config/$@.yml
	jinja2 \
	  -D beat=$@ \
	  -D elastic_version=$(ELASTIC_VERSION) \
	  templates/docker-entrypoint.j2 > build/$@/docker-entrypoint
	chmod +x build/$@/docker-entrypoint

	jinja2 \
	  -D beat=$@ \
	  -D elastic_version=$(ELASTIC_VERSION) \
	  -D url=$(DOWNLOAD_URL_ROOT)/$@/$@-$(ELASTIC_VERSION)-linux-x86_64.tar.gz \
	  -D image_flavor=full \
	  templates/Dockerfile.j2 > build/$@/Dockerfile-full
	docker build $(DOCKER_FLAGS) -f build/$@/Dockerfile-full --tag=$(REGISTRY)/beats/$@:$(VERSION_TAG) build/$@

	jinja2 \
	  -D beat=$@ \
	  -D elastic_version=$(ELASTIC_VERSION) \
	  -D url=$(DOWNLOAD_URL_ROOT)/$@/$@-oss-$(ELASTIC_VERSION)-linux-x86_64.tar.gz \
	  -D image_flavor=oss \
	  templates/Dockerfile.j2 > build/$@/Dockerfile-oss
	docker build $(DOCKER_FLAGS) -f build/$@/Dockerfile-oss --tag=$(REGISTRY)/beats/$@-oss:$(VERSION_TAG) build/$@

local-httpd:
	docker run --rm -d --name=$(HTTPD) --network=host \
	  -v $(ARTIFACTS_DIR):/mnt \
	  python:3 bash -c 'cd /mnt && python3 -m http.server'
	timeout 120 bash -c 'until curl -s localhost:8000 > /dev/null; do sleep 1; done'

release-manager-snapshot: local-httpd
	ELASTIC_VERSION=$(ELASTIC_VERSION)-SNAPSHOT \
	  DOWNLOAD_URL_ROOT=http://localhost:8000/$(BUILD_ARTIFACT_PATH) \
	  DOCKER_FLAGS='--network=host' \
	  make images || (docker kill $(HTTPD); false)
	-docker kill $(HTTPD)
release-manager-release: local-httpd
	ELASTIC_VERSION=$(ELASTIC_VERSION) \
	  DOWNLOAD_URL_ROOT=http://localhost:8000/$(BUILD_ARTIFACT_PATH) \
	  DOCKER_FLAGS='--network=host' \
	  make images || (docker kill $(HTTPD); false)
	-docker kill $(HTTPD)

# Build images from the latest snapshots on snapshots.elastic.co
from-snapshot:
	rm -rf ./snapshots
	for beat in $(BEATS); do \
	  mkdir -p snapshots/$(BUILD_ARTIFACT_PATH)/$$beat; \
	  (cd snapshots/$(BUILD_ARTIFACT_PATH)/$$beat && \
	  wget https://snapshots.elastic.co/downloads/beats/$$beat/$$beat-$(ELASTIC_VERSION)-SNAPSHOT-linux-x86_64.tar.gz && \
	  wget https://snapshots.elastic.co/downloads/beats/$$beat/$$beat-oss-$(ELASTIC_VERSION)-SNAPSHOT-linux-x86_64.tar.gz); \
	done
	ARTIFACTS_DIR=$$PWD/snapshots make release-manager-snapshot

# Push the images to the dedicated push endpoint at "push.docker.elastic.co"
push: all
	for beat in $(BEATS); do \
	  docker tag $(REGISTRY)/beats/$$beat:$(VERSION_TAG) push.$(REGISTRY)/beats/$$beat:$(VERSION_TAG); \
	  docker push push.$(REGISTRY)/beats/$$beat:$(VERSION_TAG); \
	  docker rmi push.$(REGISTRY)/beats/$$beat:$(VERSION_TAG); \
	done

# The tests are written in Python. Make a virtualenv to handle the dependencies.
venv: requirements.txt
	@if [ -z $$PYTHON3 ]; then\
	    PY3_MINOR_VER=`python3 --version 2>&1 | cut -d " " -f 2 | cut -d "." -f 2`;\
	    if (( $$PY3_MINOR_VER < 5 )); then\
		echo "Couldn't find python3 in \$PATH that is >=3.5";\
		echo "Please install python3.5 or later or explicity define the python3 executable name with \$PYTHON3";\
		echo "Exiting here";\
		exit 1;\
	    else\
		export PYTHON3="python3.$$PY3_MINOR_VER";\
	    fi;\
	fi;\
	test -d venv || virtualenv --python=$$PYTHON3 venv;\
	pip install -r requirements.txt;\
	touch venv;\

clean: venv
	docker-compose down -v || true
	rm -f docker-compose.yml build/*/Dockerfile build/*/config/*.sh build/*/docker-entrypoint
	rm -rf venv
	find . -name __pycache__ | xargs rm -rf
