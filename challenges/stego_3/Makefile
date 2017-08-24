HANDOUT=doge.jpg

include ../build.mk

doge.jpg: flag archive.zip
	cat original.jpg archive.zip > doge.jpg

archive.zip: flag
	zip archive.zip flag

flag:
	echo FLAG{Such_stego_much_flag+wow+w0w+cow} > flag

clean:
	rm -f doge.jpg archive.zip handout.tar.xz

.PHONY: clean
