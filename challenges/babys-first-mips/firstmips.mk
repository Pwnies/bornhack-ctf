CC=mips-linux-gnu-gcc
CFLAGS=-O3 -static

firstmips: firstmips.c
	$(CC) $(CFLAGS) firstmips.c -o firstmips

clean:
	rm -f firstmips .dockerid handout.tar.xz

