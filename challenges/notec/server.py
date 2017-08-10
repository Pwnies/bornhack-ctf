#!/usr/bin/python2

import os
import sys
import hashlib
import binascii
import SocketServer

# init

ADMIN_TOKEN = 'MUST NOT BE SIGNED'

with open('./flag', 'r') as f:
    flag = f.read()

# hurr durr

hs = hashlib.sha256().digest_size
hex = lambda s: binascii.hexlify(s)
unhex = lambda s: binascii.unhexlify(s)
hash = lambda s: hashlib.sha256(s).digest()
gen_priv = lambda: map(lambda _: (os.urandom(hs), os.urandom(hs)), range(hs<<3))
gen_pub = lambda priv: map(lambda (a, b): (hash(a), hash(b)), priv)
xs = lambda data: (lambda s: reduce(lambda a, b: a + b, reduce(lambda a, b: a + b, s)))(map(lambda s: map(lambda B: map(int, bin(B)[2:].zfill(8)), bytearray(s)), hash(data)))
sign = lambda data, priv: map(lambda (n, b): priv[n][b], zip(range(hs<<3), xs(data)))
verify = lambda data, sig, pub:  all(map(lambda (n, b): hash(sig[n]) == pub[n][b], zip(range(hs<<3), xs(data))))

# server

class Handler(SocketServer.StreamRequestHandler):
    def handle(self):

        # IO

        write = lambda s: self.wfile.write(s)
        readline = lambda: self.rfile.readline().strip()

        # lets sign

        key = gen_priv()
        for i in range(1, 5):
            write('[%d/4] Enter value to sign : ' % i)
            v = readline()
            if hash(v) == hash(ADMIN_TOKEN):
                write('You are not allowed to sign this')
                return
            for r in sign(v, key):
                write(hex(r) + '\n')

        # read signature

        write('Enter admin challenge:\n')
        sig = []
        for i in range(0, hs*8):
            write('[%03d] : ' % i)
            v = readline()
            try:
                if len(v) != hs*2:
                    write('Invalid signature format\n')
                    return
                sig.append(unhex(v))
            except TypeError:
                write('Invalid signature format\n')
                return

        # verify signature

        if verify(ADMIN_TOKEN, sig, gen_pub(key)) == False:
            write('Not admin, no flag\n\n\n')
            return
        write('Here is your flag : ' + flag + '\n')

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    HOST, PORT = ('0.0.0.0', 1400)
    SocketServer.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer((HOST, PORT), Handler)
    print 'Running on', HOST, ':', PORT
    server.serve_forever()

