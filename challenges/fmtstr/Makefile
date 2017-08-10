CC=gcc
CFLAGS=-O3 -pie -fPIC

include ../ports.mk

HANDOUT=fmtstr.c Makefile
DOCKER_ARGS=-p $(PORT_FMTSTR):1337
DOCKER_NAME=fmtstr
DOCKER_DEPS=fmtstr

include ../build.mk

fmtstr: fmtstr.c
	$(CC) $(CFLAGS) $< -o fmtstr
