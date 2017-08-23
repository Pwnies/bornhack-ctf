include ../ports.mk

HANDOUT=firstmips
DOCKER_NAME=firstmips
DOCKER_ARGS=-p$(PORT_FIRSTMIPS):1337
DOCKER_DEPS=firstmips run start enter-chroot

include firstmips.mk

build:
	docker build -t firstmips-build -f Dockerfile.build .
	docker run --rm -ti -v $(shell pwd):/firstmips firstmips-build

include ../build.mk

.PHONY: docker-stop docker-start docker-build clean
