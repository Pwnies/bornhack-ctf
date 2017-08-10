from pwn import *

total = 1 << 20

assert total % 4 == 0

blocks = total / 4
blocks_flag = blocks / 2

pt_len = (blocks - blocks_flag) * 4 - 1

print pt_len, '/', total

pt = 'A' * pt_len

parts = set([])

while 1:
    p = remote('127.0.0.1', 7777)
    # p = process('./birthday')
    p.sendline(pt)
    data = p.readall()

    print len(data)
    print total + 4
    assert len(data) == total + 4

    chunks = [data[n:n+4] for n in range(0, len(data), 4)]

    print blocks + 1
    print len(chunks)
    assert len(chunks) == blocks + 1

    def pair(chunks):
        return zip(chunks[1:], chunks) # (ct, iv)

    fops = pair(chunks[-blocks_flag:])
    kops = dict(pair(chunks[:-blocks_flag]))

    for i, (f_ct, f_iv) in enumerate(fops):
        try:
            k_iv = kops[f_ct]
            x = xor(k_iv, 'A' * 4)
            x = xor(x, f_iv)
            parts.add(x)
        except KeyError:
            pass

    for k in sorted(parts):
        print k






print len(data)
print len(chunks)

