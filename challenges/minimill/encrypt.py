def encrypt(data):
    x = 0x4123
    y = 0x5533

    out = []

    for pt_byte in map(ord, data):
        pt_byte ^= y
        pt_byte += x
        out.append(pt_byte & 0xff)
        new_x = ((x << 1) | (x >> 15)) & 0xffff
        new_y = ((y >> 7) | (y << 9)) & 0xffff
        new_y += x
        new_y ^= new_x
        x, y = new_x & 0xffff, new_y & 0xffff
    
    return out

import sys
sys.stdout.write("".join(map(chr, encrypt("FLAG{Next year we are having two instructions pointers one each way}\x00"))))
sys.stdout.flush()
        
