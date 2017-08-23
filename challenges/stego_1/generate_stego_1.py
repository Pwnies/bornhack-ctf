#!/usr/bin/env python2

# Script for generating the 'stego_1 challenge'
# ./generate_stego_1.py <flag>
# make sure the 'dictionary.txt' in the same folder

import random, sys

f = open("stego_1.txt","w+")
lines = open("dictionary.txt","r").read().splitlines()

for i in range(0,50000):
    myline = random.choice(lines)
    f.write(myline + "\n")
    if (i == 8215):
        f.write(sys.argv[1] + "\n")

f.close()
