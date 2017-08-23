#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# CWAT: Caesar with a twist
# By Emil S. Bak, 2017
# DIKU

import sys, getopt, random


def caesar(original, base):
    if (base > 26):
        base = base%26

    if (ord(original) == 32 ):
        return chr(ord(letter))
    elif ((ord(original) + base > ord('z')) or ( (ord(original) >= ord("A"))  and ord(original) <= ord("Z")) and ((ord(original) + base) > ord("Z"))):
        return ord(original) + base-26
    else:
        return ord(original) + base


def encrypt(originalString):

    # Variables - The Caesar Cipher is randomized (n)
    n = random.randint(1, 25)
    i = 0
    result = []

    for letter in originalString:
        i = i + n
        result.append(caesar(letter,i))

    # The Cipher is attached.
    result.append(97 + n)
    print ("".join(map(chr,result)))


def decrypt(decryptedString):

    # Ugly lazy variables
    n = 0
    result = []

    # Gets the cipher, aka the last letter from the string, and gets its value.
    cipher = ord(decryptedString[-1:]) - ord('a')
    decryptedString = decryptedString[:-1]

    for letter in decryptedString:
        n = (n + cipher)%26
        result.append(caesar(letter,26-n))

    print ("".join(map(chr,result)))


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"d:e:",["decrypt","encrypt"])
    except getopt.GetoptError:
        print ("Wrong input - Try again (-d, -e)")
        print ("cwat [-argument] [input]")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-e","--encrypt"):
            encrypt(arg)
        if opt in ("-d","--decrypt"):
            decrypt(arg)


# Main
if __name__ == '__main__':
    if not (sys.argv[2:]):
        print ("Wrong input - Try again (-d, -e)")
        print ("cwat [-argument] [input]")
        print ("    Example: python cwat -e helloworld")
    main(sys.argv[1:])






