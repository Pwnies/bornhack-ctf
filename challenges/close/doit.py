from pwn import *

conn = remote('127.0.0.1', 11111)

e = int(conn.recvline().split(':')[-1], 16)
N = int(conn.recvline().split(':')[-1], 16)
f = int(conn.recvline().split(':')[-1], 16)

print e
print N
print f

from gmpy2 import isqrt, next_prime, invert

approx = isqrt(N)

q = next_prime(approx)
assert N % q == 0
p = N // q

d = invert(e, (p-1)*(q-1))
p = pow(f, d, N)

pad = lambda x: '0' + x if len(x) % 2 else x

print pad('%x' % p).decode('hex')
