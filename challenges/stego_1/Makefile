FLAG=FLAG{HidingInPlaneSight}

HANDOUT=stego_1.txt INTRO.md

include ../build.mk

stego_1.txt: build

build:
	python generate_stego_1.py $(FLAG)

clean:
	rm -f stego_1.txt handout.tar.xz

.PHONY: clean build
