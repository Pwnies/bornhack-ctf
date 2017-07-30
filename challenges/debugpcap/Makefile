HANDOUT=debug.pcap

handout.tar.xz: $(HANDOUT)
	tar -cJf handout.tar.xz $^

flag:
	echo flag{$(shell head -c 20 /dev/urandom | xxd -ps)} > flag

debug.pcap: ./build.sh Dockerfile debuggee.sh debugger.sh gdbscript flag
	./build.sh
	

