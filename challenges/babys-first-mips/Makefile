CC=mips-linux-gnu-gcc
CFLAGS=-O3 -static

include ../ports.mk

HANDOUT=firstmips
DOCKER_NAME=firstmill
DOCKER_ARGS=-p$(PORT_FIRSTMIPS):1337
DOCKER_DEPS=firstmips run start enter-chroot

firstmips: firstmips.c
	$(CC) $(CFLAGS) firstmips.c -o firstmips

include ../build.mk

clean:
	rm -f firstmips .dockerid handout.tar.xz

.PHONY: docker-stop docker-start docker-build clean


    
