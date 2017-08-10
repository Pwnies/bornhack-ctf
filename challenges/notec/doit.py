import time
from pwn import *

col = [
    'edb49f4d0cb2dde70c6db728fddd8811',
    '4d69623c1e699f5320285cc9743272ab',
    'e6b22d8e6c3b506d2659de8adf19ee8a',
    '1bf1756c265faf95c819787764a5f6d8'
]

TARGET = 'MUST NOT BE SIGNED'
hash = lambda s: hashlib.sha256(s).digest()

def to_bits(data):
    out = ''
    for B in bytearray(data):
        out += bin(B)[2:].zfill(8)
    return out

def send_sign(p, v):
    p.sendline(v)
    out = [p.recvline().strip()[len('[1/4] Enter value to sign : '):]]
    for i in range(1, 256):
        s = p.recvline().strip()
        out.append(s)
    return out

# Oracle sign

p = remote('127.0.0.1', 1400)
signed = {to_bits(hash(c)): send_sign(p, c) for c in col}

# Sign challenge

sig = []
tar = to_bits(hash(TARGET))
for i in range(0, 256):
    for c in signed:
        if c[i] == tar[i]:
            sig.append(signed[c][i])
            break
    else:
        print 'I CANT SIGN THIS, I LACK THE BITS MAN!'
        exit(-1)

for v in sig:
    p.sendline(v)

while 1:
    line = p.recvline()
    if 'flag' in line:
        print 'A', line
        break

p.close()
