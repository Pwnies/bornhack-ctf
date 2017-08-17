#!/usr/bin/env python2.7
from hashlib import sha256

P = 72903249772034460094762354455647169031205931523248962549937113795622619810673
R = 2**20

def i2a(x):
    s = ''
    while x:
        s += chr(x & 0xff)
        x >>= 8
    return s

def a2i(s):
    x = 0
    for c in s[::-1]:
        x <<= 8
        x |= ord(c)
    return x

def kdf(password):
    return a2i(sha256(password).digest()) % P

def crypto(magic):
    def f(text, password):
        k = kdf(password)
        a = a2i(text)
        b = 0
        while a:
            x = a % P
            for _ in xrange(R):
                x = magic(x, k)
            b *= P
            b += x
            a /= P
        return i2a(b)
    return f

@crypto
def enc(x, k):
    x = (x + k) % P
    x = (x * 1337) % P
    return x

@crypto
def dec(x, k):
    # TODO: implement this
    return 0

if __name__ == '__main__':
    import signal
    import sys
    signal.alarm(50)
    PASSWORD = file('PASSWORD').read().strip()
    plaintext = ''
    while True:
        s = sys.stdin.read()
        if not s:
            break
        plaintext += s
    sys.stdout.write(enc(plaintext, PASSWORD))
