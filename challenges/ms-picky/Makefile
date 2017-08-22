TARGET:=ms-picky

ARCH:=amd64
# ARCH:=i386

all: $(TARGET)

CFLAGS+=-ffreestanding -fno-common -fPIE
ASFLAGS+=-fPIE
LDFLAGS=
LDLIBS=-lcrypto

# SRCS:=init.c lib.c malloc.c sha1.c lzss.c sqz.c map.c longjmp.c debug.c
SRCS:=loader.c
ARCH_OBJS:=start.o syscalls.o

OBJS:=$(patsubst %.c, %.o, $(SRCS))

ifeq ($(ARCH), i386)
CC=gcc
LD=ld
AS=as
OBJCOPY=objcopy
STRIP=strip
CFLAGS+=-m32
LDFLAGS+=-melf_i386
NASMFLAGS+=-felf
OBJS+=$(patsubst %.o, %_i386.o, $(ARCH_OBJS))
endif

ifeq ($(ARCH), amd64)
CC=gcc
LD=ld
AS=as
OBJCOPY=objcopy
STRIP=strip
CFLAGS+=-m64
LDFLAGS+=-melf_x86_64
NASMFLAGS+=-felf64
OBJS+=$(patsubst %.o, %_amd64.o, $(ARCH_OBJS))
endif


ifdef DEBUG
CFLAGS+=-DPRINTF -DDEBUG=$(DEBUG)
OBJS+=xprintf.o
endif

ifdef TESTING
CFLAGS+=-DTESTING -g
endif

.PHONY: clean
# .INTERMEDIATE: dummy.o

clean:
	rm -f *.so *.o *.sc *.enc *.inc syscalls_*.asm inner $(TARGET) \
	peda-session-*

inner: inner.c
	gcc $^ -o $@ -lcrypto

# inner: hello.c
# 	gcc $^ -o $@ -static

%.inc: %
	xxd -i < $< > $@

%.enc: %
	python encode.py $< > $@

# `inner.enc.inc` must come before `$(OBJS)` because it is needed by the loader
ms-picky.sc: shellcode.ld inner.enc.inc $(OBJS)
	$(LD) $(LDFLAGS) --build-id=none -T shellcode.ld $(OBJS) -o dummy.o
	$(OBJCOPY) -j .shellcode -O binary dummy.o $@
	chmod -x $@
	rm dummy.o

syscalls_%.asm: syscalls.h
	./syscalls.py $< $@

%.o: %.asm
	nasm $(NASMFLAGS) $< -o $@

%: %.sc
	python sc2elf.py $< > $@
	chmod +x $@
