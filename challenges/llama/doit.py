from math import factorial

N = 0x6c6c616d612c6c6c616d612c6c6c616d61

def a(n):
    tot = 5
    while n:
        if n == 1:
            break
        else:
            tot *= factorial(n)
        n -= 1
        tot %= N
        print n, '%x' % tot
    return tot

print 'flag{%x}' % a(0x1337)
