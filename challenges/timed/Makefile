HANDOUT=server.py

include ../ports.mk

DOCKER_ARGS=-p $(PORT_TIMED):1337
DOCKER_NAME=timed
DOCKER_DEPS=timed

include ../build.mk

timed: server.py flag
