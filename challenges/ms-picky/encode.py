import sys

fi = file(sys.argv[1])
fo = sys.stdout
k = 0xff
while True:
    c = fi.read(1)
    if not c:
        break
    c = chr(ord(c) ^ k)
    k = (k - 1) & 0xff
    fo.write(c)
