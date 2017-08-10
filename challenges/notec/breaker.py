import hashlib
import os
import binascii

### PART OF DOIT! DO NOT HAND OUT!!! ###

"""
Probability of finding a match:
> 1 / (1 - (1/2.)**m)**bit
m   = messages signed by oracle
bit = hash digest size

Collision found (for 4 messages):
edb49f4d0cb2dde70c6db728fddd8811
4d69623c1e699f5320285cc9743272ab
e6b22d8e6c3b506d2659de8adf19ee8a
1bf1756c265faf95c819787764a5f6d8
"""

TARGET = 'MUST NOT BE SIGNED'
hash = lambda s: hashlib.sha256(s).digest()
hash_size = 256
hex = lambda s: binascii.hexlify(s)

def to_bits(data):
    out = ''
    for B in bytearray(data):
        out += bin(B)[2:].zfill(8)
    return out

rand = lambda: hex(os.urandom(16))
tar = to_bits(hash(TARGET))
tried = 0

while 1:
    ins = [rand() for i in range(0, 4)]
    vec = map(to_bits, map(hash, ins))
    for i in range(0, hash_size):
        for v in vec:
            if v[i] == tar[i]:
                break
        else:
            break
    else:
        print 'You win!'
        print 'Have them sign these strings:'
        for val in ins:
            print  val
        exit(0)

    tried += 1
    if tried % 10000 == 0:
        print tried
