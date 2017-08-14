#!/usr/bin/env python2.7
import gmpy2
import sys

from main import *

# Closed form of `enc`:
# ct = pt * 1337**R + sum(k * 1337**i for i = 1..R)

# A = 1337**R
A = gmpy2.powmod(1337, R, P)

# B = 1337**R + 1337**(R - 1) + ... + 1337
#   = (1337**(R + 1) - 1) / (1337 - 1) - 1
B = gmpy2.divm(gmpy2.powmod(1337, R + 1, P) - 1, 1336, P) - 1

pt = a2i(file('lorem').read()) % P
ct = a2i(file('lorem.enc').read())
# Caveat: corresponding CT block is the most significant part
while ct > P:
    ct /= P

# Solve for k
k = gmpy2.divm(ct - A * pt, B, P)

def dec(ct, k):
    a = a2i(ct)
    b = 0
    while a:
        x = a % P
        # Solve for pt
        x = gmpy2.divm(x - B * k, A, P)
        b *= P
        b += x
        a /= P
    return i2a(b)

sys.stdout.write(dec(file('FLAG.enc').read(), k))
# sys.stdout.write(dec(file('lorem.enc').read(), k))
