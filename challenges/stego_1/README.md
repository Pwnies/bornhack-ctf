Stego_1:
========
	Another easy introduction to the art of stego (steganography).
	The user is presented with a dictionary (not in alphabetical order),
	and must find the flag! But more than a simple 'ctrl + f' is needed...!

Flag:
=====
	flag{Good job! THIS is the flag!}

Solution:
=========
	grep 'flag' stego_1.txt | sort | uniq -u
	OR
	grep flag{.*} stego_1.txt


Author:
=======
	Emil 'Dota' Bak
		emilsbak@gmail.com
	René 'Lurpak' Jacobsen
		rlj@rloewe.net

Tags:
=====
	stego, easy, forensics