HANDOUT=debug.pcap

include ../build.mk

flag:
	echo flag{$(shell head -c 20 /dev/urandom | xxd -ps)} > flag

debug.pcap: ./build.sh Dockerfile debuggee.sh debugger.sh gdbscript flag
	./build.sh

clean:
	rm -f handout.tar.xz debug.pcap
