Stego_3:
========
	Presented with a picture of our glorious
	Lord and Saviour, Doge, find the secret flag.


Flag:
=====
	flag{Such stego, much flag, wow}


Solution:
=========
	1: Detect the zip folder (binwalk, xxd doge.jpg & find 'PK' in the hexDump, etc)
		xxd doge.jpg
	2: Take the hex value of the line where you find 'PK' (indicating a zip-file start),
	   after FFD9 (which is the end of a jpg file).
		00008480
	3: Run the DD command with the new dec value
		dd if=doge.jpg bs=1 skip=$[8480] of=foo.zip
	4: Unzip foo.zip and cat the remaining .txt file
		unzip foo.zip & cat secret.txt


Author:
=======
	Emil 'Dota' Bak
		emilsbak@gmail.com


Tags:
=====
	stego, medium, obscure