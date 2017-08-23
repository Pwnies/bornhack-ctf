HANDOUT=brainfuck

CC=gcc
CFLAGS=-O3
STRIP=strip

brainfuck: brainfuck.c chal.h
	$(CC) $(CFLAGS) brainfuck.c -o brainfuck
	$(STRIP) -s brainfuck

chal.h: chal.bf
	xxd -i chal.bf > chal.h

chal.bf: generate.py flag
	python generate.py > chal.bf

flag:
	echo FLAG{$(shell head -c 20 /dev/urandom | xxd -ps)} > flag

clean:
	rm -f chal.h chal.bf brainfuck handout.tar.xz

include ../build.mk

