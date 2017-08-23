# Script for generating the 'stego_1 challenge'
# ./generate_stego_1.py
# make sure the 'dictionary.txt' in the same folder

import random

f = open("stego_1.txt","a")

lines = open('dictionary.txt').read().splitlines()
for i in range(0,50000):
    myline =random.choice(lines)
    f.write(myline + "\n")
    if (i == 8215):
    	f.write("FLAG{HidingInPlainSight} \n")

f.close()