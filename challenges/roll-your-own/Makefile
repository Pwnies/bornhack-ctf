HANDOUT=flag.enc main.py lorem.enc lorem

include ../build.mk

PASSWORD:
	head -c 20 /dev/urandom | xxd -ps > PASSWORD

flag.enc: flag PASSWORD
	python main.py < flag > flag.enc

lorem.enc: lorem PASSWORD
	python main.py < lorem > lorem.enc

flag:
	echo flag{$(shell head -c 20 /dev/urandom | xxd -ps)} > flag

clean:
	rm -f *.enc flag PASSWORD handout.tar.xz
