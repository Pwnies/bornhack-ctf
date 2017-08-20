CWAT:
========
	The fameous Caesar cipher, but with a twist or two...!


Flag:
=====
	flag{FurthermoreIBelieveThatJavaMustBeDestroyed}


Explanation:
=========
	0: The 'cwat' encryption works like caesars, except instead of shifting a
	   whole word (aka all letters) with the same cipher, 'cwat' instead shifts
	   every letter with an ever increasing cipher.

	1: This increasing cipher (n) is put at the end of an encrypted word, and its
	   value is the distance from the letter a (so if an encrypted word ended with
	   a 'g', the cipher would be 6.

	2: Thus encrypting 'abc' with the cipher 2, would result in 'cfic'.
	   The first letter in the encrypted word is 'c', since 'a' shifted 2 is 'c',
	   however, the following word 'f', is the original b having shifted 4.
	   This is due to the cipher being cumulative. If the cipher is 2, it will shift
	   letters [2,4,6,8,10,12,14,...] respectivly, and add the cipher (obscured as a
	   letter) at the end.

	   'abc' -> 'cfic'


Solution:
=========
	0: Given either a few examples, or free access to the encryption part, the contestant
	   should notice that a letter has been added to the given encrypted words, and that
	   a simple Caesar deciphering is not enough to solve it. Preferably, the contestant
	   will try creating his own caesar-decyphering implementation, and quickly figure out
	   that the added last letter has something to do with the cipher.

	1: The easiest way to decpiher a shiftet letter, is to simply shift it again using
	   [26-n], n being the cipher, and 26 being the letters in the alphabet.


Author:
=======
	Emil 'Dota' Bak (Pwnies)
		emilsbak@gmail.com


Tags:
=====
	easy, obscure, crypto, programming