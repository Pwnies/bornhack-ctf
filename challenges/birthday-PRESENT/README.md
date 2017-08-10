# Birthday PRESENT

Crypto challenge.

The challenge is inspired by the [Sweet32](https://sweet32.info/) attack on 64-bit block ciphers in SSL/TLS.
The block size has been reduced to 32-bit to make the attack more practical.

The difficulty is Medium / Easy.
On the level with Set 3 in Cryptopals.

## Running the challenge

### Handout

The player should be given:

  - Makefile
  - mk_flag.py (or have the peculiar format explained to them)
  - main.c

A doit has been included as proof of "solvability".
This, of course, SHOULD NOT be handed out, neither should "flag"...

### Running the server

Simply "make" the challenge and run ./run.sh
Which will bind to 0.0.0.0:47806
Challenge requires "socat"

Dockerfile is also provided.

## Flag

The flag format is different due to the nature of the challenge (explained in doc).
The flag is pieced together from a number of 4 byte chunks,
the first 2 bytes of which is the index (in ascii) of the following two bytes in the flag:

    00fl
    01ag
    02{H
    03ap
    04py
    05Bi
    06rt
    07hd
    08ay
    09To
    10Yo
    11u}

Which reads as:

    flag{HappyBirthdayToYou}

This latter string is the flag to be handed in.
Of course the 4-byte blocks may be permuted, the player should deal with this.

## Required knowledge

  - Programming
  - Some familiarity with block ciphers (and CBC mode)
  - The ability to read C

## Tags

  crypto, medium, cbc, sweet32
