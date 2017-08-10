#!/usr/bin/python2

import os
import SocketServer

from gmpy2 import invert, next_prime
from random import randrange
from hashlib import sha256

KEY_SIZE = 3072

def gen_primes():
    n = int(os.urandom(KEY_SIZE // 16).encode('hex'), 16)
    n = next_prime(n)
    while 1:
        yield n
        n = next_prime(n)

with open('./flag', 'r') as f:
    flag = f.read().strip()

class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        write = lambda s: self.wfile.write(s)
        readline = lambda: self.rfile.readline().strip()

        # pad

        flagx = flag + ' | ' + os.urandom(128).encode('hex')
        flagx = int(flagx.encode('hex'), 16)

        # generate RSA key

        g = gen_primes()
        p = next(g)
        q = next(g)
        N = p * q
        e = 65537
        d = invert(e, (p-1)*(q-1))

        if flagx > N:
            write('I failed sorry')
            return

        # encrypt

        write('e    : %x\n' % e)
        write('N    : %x\n' % N)
        write('flag : %x\n' % pow(flagx, e, N))

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    HOST, PORT = ('0.0.0.0', 1337)
    SocketServer.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer((HOST, PORT), Handler)
    print 'Running on', HOST, ':', PORT
    server.serve_forever()
