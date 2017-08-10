#!/usr/bin/env python2

'''
This file converts the flag to the challenge format.
The flag is converted into 32-bit chops,
starting with 2 ascii characters giving the index of the slice.
eg.:

    read from "flag"
    ->
    hellothere
    ->
    he ll ot he re
    ->
    00he 01ll 02ot 03he 04re
    ->
    00he01ll02ot03he04re
    ->
    save to "flag.fmt"

'''

with open('flag', 'r') as f:
    raw = f.read().strip()

assert len(raw) % 2 == 0

raw = [raw[n:n+2] for n in range(0, len(raw), 2)]
raw = ['%02d%s' % (i, x) for (i, x) in zip(range(len(raw)), raw)]

flag = ''.join(raw)

with open('flag.fmt', 'w') as f:
    f.write(flag)
