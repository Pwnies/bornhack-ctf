CC=gcc
CFLAGS=-O3 -pie -fPIC

include ../ports.mk

HANDOUT=INTRO.md Makefile
DOCKER_ARGS=-p $(PORT_UTM):1337
DOCKER_NAME=utm
DOCKER_DEPS=run-turing.py run

include ../build.mk
