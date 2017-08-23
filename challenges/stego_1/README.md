Stego_1:
========
    Another easy introduction to the art of stego (steganography).
    The user is presented with a dictionary (not in alphabetical order),
    and must find the flag! But more than a simple 'ctrl + f' is needed...!

Flag:
=====
    FLAG{HidingInPlainSight}

Solution:
=========
    grep 'FLAG' stego_1.txt | sort | uniq -u
    OR
    grep FLAG{.*} stego_1.txt


Author:
=======
    Emil 'Dota' Bak (Pwnies)
        emilsbak@gmail.com
    René 'Lurpak' Jacobsen (Pwnies)
        rlj@rloewe.net

Tags:
=====
    stego, easy, forensics
