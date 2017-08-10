CC=gcc
CFLAGS=-std=c11
HANDOUT=server.py

include ../ports.mk

DOCKER_ARGS=-p $(PORT_CLOSE):1337
DOCKER_NAME=close
DOCKER_DEPS=server.py flag

include ../build.mk

close: server.py flag
