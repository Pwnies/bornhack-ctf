#!/usr/bin/env python2
import socket

HOST='ctf.pwnies.dk'

lines = open('challenges/ports.mk').read().strip().split('\n')
lines = filter(lambda s: not s.strip().startswith('#'), lines)
ports = [ line.split('=') for line in lines ]

for (name,port) in ports:
    name = name[5:]
    port = int(port)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((HOST, port))
        print "\x1b[0;32m{0:>10} {1:>5} UP\x1b[0m".format(name, port)
    except socket.error:
        print "\x1b[0;31m{0:>10} {1:>5} DOWN\x1b[0m".format(name, port)
