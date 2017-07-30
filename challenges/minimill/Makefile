CC=gcc
CFLAGS=-m32 -no-pie
STRIP=strip

HANDOUT=minimill

handout.tar.xz: $(HANDOUT)
	tar -cJf handout.tar.xz $^

minimill: minimill.c rom.h
	$(CC) $(CFLAGS) $< -o minimill
	$(STRIP) -s minimill

firmware.bin: asm.py firmware.asm
	python asm.py firmware.asm firmware.bin

flag.bin: encrypt.py
	python encrypt.py > flag.bin

rom.bin: firmware.bin flag.bin
	cat $^ > $@

rom.h: rom.bin
	xxd -i rom.bin > rom.h

clean:
	rm -f firmware.bin flag.bin rom.bin rom.h minimill handout.tar.xz
