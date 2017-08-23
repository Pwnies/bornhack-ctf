HANDOUT=debug.pcap

include ../build.mk

flag:
	echo FLAG{GdBs_protocol_is_the_epitome_of_design_beauty!} > flag

debug.pcap: ./build.sh Dockerfile debuggee.sh debugger.sh gdbscript flag
	./build.sh

clean:
	rm -f handout.tar.xz debug.pcap
