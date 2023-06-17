.PHONY: default deps base build stop shell test demo-terminal demo-image run-stats

export SERVICE_NAME := mazes-for-programmers

BUILD_ENV ?= dev

HISTORY_FILE := ~/.bash_history.$(SERVICE_NAME)

# Required for the `deps` task
SHELL := $(shell which bash)

DOCKER := $(shell command -v docker)
COMPOSE := $(shell command -v docker) compose

COMPOSE_ENV := $(COMPOSE) -f build/$(BUILD_ENV)/docker-compose.yml
COMPOSE_CMD := $(COMPOSE_ENV) run --rm $(SERVICE_NAME)

export GID := $(shell id -g)
export UID := $(shell id -u)

deps:
ifndef DOCKER
	@echo "Docker is not available. Please install docker"
	@exit 1
endif
ifndef COMPOSE
	@echo "docker-compose is not available. Please install docker-compose"
	@exit 1
endif
	@touch $(HISTORY_FILE)

base: deps
	$(COMPOSE) -f build/base/docker-compose.yml build

build: base
	$(COMPOSE_ENV) build

stop:
	$(COMPOSE_ENV) stop
	$(COMPOSE_ENV) rm -f -v

shell: build
	$(COMPOSE_CMD) /bin/bash

test: build
	set -o pipefail; \
	$(COMPOSE_CMD) pytest

demo-terminal: build
	$(COMPOSE_CMD) python3 demos/terminal_demo.py $(rows) $(cols) $(algorithm) $(exporter) $(rotations) $(pathfinding)

demo-image: build
	$(COMPOSE_CMD) python3 demos/image_demo.py $(rows) $(cols) $(algorithm) $(exporter) $(rotations) $(pathfinding) $(coloring)

demo-game-map: build
	$(COMPOSE_CMD) python3 demos/game_map_demo.py $(rows) $(cols) $(algorithm)

run-stats: build
	$(COMPOSE_CMD) python3 demos/stats_demo.py $(rows) $(cols) --tries=$(tries) --pathfinding=true
