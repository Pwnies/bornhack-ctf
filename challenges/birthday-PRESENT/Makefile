CC=gcc
CFLAGS=-std=c11
HANDOUT=main.c mk_flag.py

include ../ports.mk

DOCKER_ARGS=-p $(PORT_BIRTHDAY):1337
DOCKER_NAME=birthday
DOCKER_DEPS=birthday

include ../build.mk

birthday: flag main.c mk_flag.py
	python mk_flag.py flag flag.fmt
	$(CC) $(CFLAGS) main.c -o birthday

clean:
	rm -f birthday
	rm -f handout.tar.xz
	rm -f flag.fmt
