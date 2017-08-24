HANDOUT=ultracomputer

include ../build.mk

ultracomputer: main.c magic.c
	gcc -o $@ $^  -fno-common -fno-zero-initialized-in-bss
	strip -w -s -K fini -K f[0-9]* $@
	python obfu.py

clean:
	rm -f ultracomputer handout.tar.xz

.PHONY: clean
