CC=gcc
CFLAGS=-m32 -g

minimill: minimill.c rom.h
	$(CC) $(CFLAGS) $< -o minimill

firmware.bin: asm.py firmware.asm
	python asm.py firmware.asm firmware.bin

flag.bin: encrypt.py
	python encrypt.py > flag.bin

rom.bin: firmware.bin flag.bin
	cat $^ > $@

rom.h: rom.bin
	xxd -i rom.bin > rom.h
