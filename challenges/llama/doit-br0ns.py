# Can I have a llama? (and a larger stack?)
# hint: https://www.youtube.com/watch?v=bHNczNvOnGc

Y = lambda f: f (lambda x: Y(f)(x))
M = lambda f: lambda (n, m): 0 if not n else m + f((n-1, m))
C = lambda f: lambda n: 1 if not n else Y(M)((n, f(n-1)))
A = lambda f: lambda n: 5 if not (n >> 1) else Y(M)((f(n-1), Y(C)(n)))

l = 0x6c6c616d612c6c6c616d612c6c6c616d61

def M(n, m):
    if n:
        return m + M(n - 1, m)
    else:
        return 0
def M(n, m):
    return n * m

def C(n):
    if n:
        return M(n, C(n - 1))
    else:
        return 1
def C(n):
    x = 1
    while n:
        x *= n
        n -= 1
        x %= l
    return x

def A(n):
    if n >> 1:
        return M(A(n - 1), C(n))
    else:
        return 5
def A(n):
    x = 5
    while n:
        x *= C(n)
        n -= 1
        x %= l
    return x

# g = lambda x: Y(A)(x) % l
print 'FLAG{%x}' % (A(0x1337) % l)

# flag = '{%x}' % g(0x1337)
# print 'flag:', flag
