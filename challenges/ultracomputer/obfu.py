#!/usr/bin/env python2.7
import os
from elftools.elf.elffile import ELFFile

TARGET = 'ultracomputer'

fd = file(TARGET, 'r+')
elf = ELFFile(file(TARGET))
symtab = elf.get_section_by_name('.symtab')

def obfu(name):
    sym = symtab.get_symbol_by_name(name)[0]
    fd.seek(sym.entry.st_value, os.SEEK_SET)
    data = fd.read(sym.entry.st_size)
    fd.seek(sym.entry.st_value, os.SEEK_SET)
    for i, c in enumerate(data, sym.entry.st_value):
        c = chr(ord(c) ^ (i & 0xff))
        fd.write(c)

obfu('fini')
n = 0
while True:
    try:
        obfu('f%02d' % n)
    except:
        break
    n += 1

fd.close()
