***************************************
**    WELCOME TO TETRIS CHALLENGE    **
***************************************


Purpose of the exercise

In TETRIS challenge you will receive something like this:
0000000000
0000000000
0000000000
0000000000
00000X0X00
0XXXXXXXX0
XXXXX0XXXX
XXX0XXXXXX
0XXX0XXXX0
0XXX0X00X0

And as a valid response, you could send back something like this:
0000000000
0000000000
0000000000
0000000000
00000g0j00
0hhfggjji0
hhffg0ejii
ddf0cceeai
0ddb0ceaa0
0bbb0c00a0

The challenge is about finding possible ways to place 10 tetris blocks in a 10X10 squared frame. You receive the frame filled with 0's and X's. The X's should be substituted with tetris blocks. A tetris block has a size of 4 squares and actually every possible combination of 4 squares represents a specific tetris block. You should not replace the 0's. In order to be able to distinguish the blocks from each other, give every block a uniqe letter between a and j in the alphabet.

To get the flag, you need to fill out 100 different tetris frames. There will be a time limit, so do not bother to try solving this exercise manually.


Data format

You receive:
A multidimentional list of 10X10 ascii characters.
Every element is either the char '0' or the char 'X'.
The list is json encoded and then byte encoded before it is send.

You respond with:
A multidimentional list of 10X10 ascii characters.
Every element should either be the char '0', or a char value between 'a' and 'j' (lowercase).
The list should be json encoded and then byte encoded before is is send.


Server connection


In order to receive frames and send solutions, you have to connect to a server running on:
IP      ????
PORT    ????


