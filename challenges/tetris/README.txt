***************************************
**    WELCOME TO TETRIS CHALLENGE    **
***************************************


Purpose of the exercise

In TETRIS challenge you will receive something like this:
00000000
00000000
00000000
000X0000
X00XX000
XXX0XX00
XXXXXXXX
XXXXX0XX


And as a valid response, you could send back something like this:
00000000
00000000
00000000
000e0000
f00ee000
fff0ed00
ccadddbb
ccaaa0bb

The challenge is about finding possible ways to place 6 tetris blocks in a 8X8 squared frame. You receive the frame filled with 0's and X's. The X's should be substituted with tetris blocks. A tetris block has a size of 4 squares and actually every possible combination of 4 squares represents a specific tetris block. You should not replace the 0's. In order to be able to distinguish the blocks from each other, give every block a uniqe letter between a and f in the alphabet.

To get the flag, you need to fill out 100 different tetris frames. There will be a time limit, so do not bother to try solving this exercise manually.


Data format

You receive:
A multidimentional list of 8X8 ascii characters.
Every element is either the char '0' or the char 'X'.
The list is json encoded and then byte encoded before it is send.

You respond with:
A multidimentional list of 8X8 ascii characters.
Every element should either be the char '0', or a char value between 'a' and 'f' (lowercase).
The list should be json encoded and then byte encoded before is is send.


Server connection


In order to receive frames and send solutions, you have to connect to a server running on:
IP      ????
PORT    ????


