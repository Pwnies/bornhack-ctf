DEBUG = False

if DEBUG:
    A = 1
    B = 1
    C = 3
    D = 1
    E = 1
    X = 5
else:
    A = 2824347577
    B = 3808051021
    C = 2834384563
    D = 3483568087
    E = 3475818217
    X = 670617279

FLAG = [0] * 5
N = 0
STEPS = 0

def step():
    global N, STEPS
    print 'STEP'
    N += 1
    STEPS += 1
    FLAG[0] = (FLAG[0] + A) & 0xffffffff
    STEPS += A + 1
    FLAG[1] = (FLAG[1] + B) & 0xffffffff
    STEPS += B + 1
    FLAG[2] = (FLAG[2] + C) & 0xffffffff
    STEPS += C + 1
    FLAG[3] = (FLAG[3] + D) & 0xffffffff
    STEPS += D + 1
    FLAG[4] = (FLAG[4] + E) & 0xffffffff
    STEPS += E + 1

def odd():
    global STEPS
    print 'ODD'

    print ' STEPS = %d' % STEPS
    print ' F1 += F0 = 0x%08x + 0x%08x' % (FLAG[1], FLAG[0])
    STEPS += 2 + 2 * FLAG[0]
    FLAG[1] = (FLAG[1] + FLAG[0]) & 0xffffffff

    print ' STEPS = %d' % STEPS
    print ' F2 -= F1 = 0x%08x - 0x%08x' % (FLAG[2], FLAG[1])
    STEPS += 2 + 2 * FLAG[1]
    FLAG[2] = (FLAG[2] - FLAG[1]) & 0xffffffff

    print ' STEPS = %d' % STEPS
    print ' F3 *= F2 = 0x%08x * 0x%08x' % (FLAG[3], FLAG[2])
    STEPS += 4 + (4 + 2 * FLAG[3]) * FLAG[2]
    FLAG[3] = (FLAG[3] * FLAG[2]) & 0xffffffff

    print ' STEPS = %d' % STEPS
    print ' F4 ^= F3 = 0x%08x ^ 0x%08x' % (FLAG[4], FLAG[3])
    STEPS += 2 + 2 * 32
    FLAG[4] ^= FLAG[3]

def even():
    global STEPS
    print 'EVEN'

    print ' STEPS = %d' % STEPS
    print ' F3 += F4 = 0x%08x + 0x%08x' % (FLAG[3], FLAG[4])
    STEPS += 2 + 2 * FLAG[4]
    FLAG[3] = (FLAG[3] + FLAG[4]) & 0xffffffff

    print ' STEPS = %d' % STEPS
    print ' F2 -= F3 = 0x%08x - 0x%08x' % (FLAG[2], FLAG[3])
    STEPS += 2 + 2 * FLAG[3]
    FLAG[2] = (FLAG[2] - FLAG[3]) & 0xffffffff

    print ' STEPS = %d' % STEPS
    print ' F1 *= F2 = 0x%08x * 0x%08x' % (FLAG[1], FLAG[2])
    STEPS += 4 + (4 + 2 * FLAG[1]) * FLAG[2]
    FLAG[1] = (FLAG[1] * FLAG[2]) & 0xffffffff

    print ' STEPS = %d' % STEPS
    print ' F0 ^= F1 = 0x%08x ^ 0x%08x' % (FLAG[0], FLAG[1])
    STEPS += 2 + 2 * 32
    FLAG[0] ^= FLAG[1]

def collatz(x):
    global STEPS
    while True:
        print ' F0 = 0x%08x, F1 = 0x%08x, F2 = 0x%08x, F3 = 0x%08x, F4 = 0x%08x' % tuple(FLAG)
        step()
        print ' X = %d, N = %d, STEPS = %d' % (x, N, STEPS)
        print ' F0 = 0x%08x, F1 = 0x%08x, F2 = 0x%08x, F3 = 0x%08x, F4 = 0x%08x' % tuple(FLAG)
        STEPS += 1
        if x == 1:
            break
        STEPS += 1
        if x & 1:
            STEPS += 2
            x = x * 3 + 1
            odd()
        else:
            STEPS += 1
            x = x / 2
            even()
    print ' STEPS =', STEPS
    print 'FLAG{%08x%08x%08x%08x%08x}' % tuple(FLAG)

collatz(X)
