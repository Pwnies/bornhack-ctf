HANDOUT=stego_0.bmp

include ../build.mk

stego_0.bmp: flag
	cat original.bmp flag > stego_0.bmp

flag:
	echo FLAG{Ur_an_H4x0r_Harold!!1} > flag

clean:
	rm -f stego_0.bmp handout.tar.xz

.PHONY: clean
