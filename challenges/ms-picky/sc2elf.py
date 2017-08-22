#!/usr/bin/env python2.7
import struct
import sys

def b(x):
    return struct.pack('B', x)
def h(x):
    return struct.pack('H', x)
def w(x):
    return struct.pack('I', x)
def q(x):
    return struct.pack('Q', x)

ELFCLASS64    = 2
ELFDATA2LSB   = 1
ELFOSABI_SYSV = 0
EI_NIDENT     = 0x10
EV_CURRENT    = 1
ET_EXEC       = 2
ET_DYN        = 3
EM_X86_64     = 62
PT_NULL       = 0
PT_LOAD       = 1
PT_INTERP     = 3
PF_X          = 1
PF_W          = 2
PF_R          = 4

DATA = ''.join(file(x).read() for x in sys.argv[1:])

# EHDR
elf  = '\x7fELF'             # e_ident
elf += b(ELFCLASS64)
elf += b(ELFDATA2LSB)
elf += b(EV_CURRENT)
elf += b(ELFOSABI_SYSV)
elf += b(0)                  # ABI version
elf  = elf.ljust(EI_NIDENT, '\x00')
elf += h(ET_DYN)             # e_type
elf += h(EM_X86_64)          # e_machine
elf += w(EV_CURRENT)         # e_version
elf += q(0x78)               # e_entry
elf += q(0x40)               # e_phoff
elf += q(0)                  # e_shoff
elf += w(0)                  # e_flags
elf += h(0x40)               # e_ehsize
elf += h(0x38)               # e_phentsize
elf += h(1)                  # e_phnum
elf += h(0)                  # e_shentsize
elf += h(0)                  # e_shnum
elf += h(0)                  # e_shstrndx

# PHDR
elf += w(PT_LOAD)            # p_type
elf += w(PF_R | PF_W | PF_X) # p_flags
elf += q(0x78)               # p_offset
elf += q(0x78)               # p_vaddr
elf += q(0)                  # p_paddr
elf += q(len(DATA))          # p_filesz
elf += q(len(DATA))          # p_memsz
elf += q(0)                  # p_align

# Segment
elf += DATA

sys.stdout.write(elf)
