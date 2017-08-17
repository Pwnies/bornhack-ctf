#!/usr/bin/env python2

from unicorn import *
from unicorn.x86_const import *

import SocketServer

ADDRESS  = 0x10000
MEMORY   = 4 * 1024
STACK    = ADDRESS + MEMORY / 2
WORDSIZE = 4

def pad_to_word(s):
    if len(s) % WORDSIZE:
        return s + ' ' * (WORDSIZE - len(s) % WORDSIZE)
    return s

with open('flag', 'r') as f:
    flag = f.read().strip()
    flag = pad_to_word(flag)
    flag = flag + '\x00' * WORDSIZE

class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        code = self.rfile.readline().strip().decode('hex')
        try:
            mu = Uc(UC_ARCH_X86, UC_MODE_32)
            mu.mem_map(ADDRESS, MEMORY)
            mu.mem_write(ADDRESS, code)
            mu.mem_write(STACK, flag)
            mu.reg_write(UC_X86_REG_ESP, STACK)
            mu.emu_start(
                ADDRESS,
                ADDRESS + len(code),
                timeout=5*UC_SECOND_SCALE,
            )
        except UcError as e:
            pass

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    HOST, PORT = ('0.0.0.0', 1337)
    SocketServer.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer((HOST, PORT), Handler)
    server.serve_forever()
