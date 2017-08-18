# Can I have a llama? (and a larger stack?)
# hint: https://www.youtube.com/watch?v=bHNczNvOnGc

Y = lambda f: f (lambda x: Y(f)(x))
M = lambda f: lambda (n, m): 0 if not n else m + f((n-1, m))
C = lambda f: lambda n: 1 if not n else Y(M)((n, f(n-1)))
A = lambda f: lambda n: 5 if not (n >> 1) else Y(M)((f(n-1), Y(C)(n)))

l = 0x6c6c616d612c6c6c616d612c6c6c616d61
g = lambda x: Y(A)(x) % l

flag = 'FLAG{%x}' % g(0x1337)
print 'flag:', flag
