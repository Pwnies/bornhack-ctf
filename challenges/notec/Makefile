CC=gcc
CFLAGS=-std=c11
HANDOUT=server.py

include ../ports.mk

DOCKER_ARGS=-p $(PORT_NOTEC):1400
DOCKER_NAME=notec
DOCKER_DEPS=notec

include ../build.mk

notec: server.py flag
