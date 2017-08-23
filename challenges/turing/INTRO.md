Introduction:
=============
    Universal Turing Machines(UTM) can do anything! Or so everyone tells me, time for you to prove it!
    Would you mind sending me a transistion table for an UTM? It can have unlimited states and the tape alphabet has three symbols (blank, zero, one).

    I would like to recieve this encoded in the spirit of Turing.
    https://en.wikipedia.org/wiki/Universal_Turing_machine#Example_of_universal-machine_coding
    However, since several numbers have to be produced by your machine, some additions have been made:
     * The state 'DA' is the starting state and 'DH' is the halting state.
     * Integers are stored in big endian format, starting and ending with a blank character.
     * The tape is 5000 cells big, and the tape header starts at 2500.

    The machine should calculate the next term of the collatz sequence. The starting integer is placed between two blanks with the tapehead pointed at the first blank character. To avoid moving numbers around too much around, the machine should halt after each iteration of collatz.

    To simplify the process the given number is always big enough to contain every number in the (current) collatz chain.
    So if the starting number is 21 [b,1,0,1,0,1,b], the largest number is 64 [b,1,0,0,0,0,0,0,b].
    Thus the starting tape will look like this: [b,0,0,1,0,1,0,1,b]

    Collatz sequence:
    if the given integer n is even, the next number is n/2
    if the given integer n is uneven, the output is 3*n +1

    An example:
    With this given tape represtenting the binary number 4:
    [b,1,0,0,b]
    The output after your machine is run should be the binary number 2.
    [b,0,1,0,b]
    
    Simple example of a turing machine, which calculates a not operation on a given number
    The syntax for this pseudocode is `statename,tape symbol, symbol to print, next sate`
    ```start,b,b,r,not
    not,0,1,r,not
    not,1,0,r,not
    not,b,b,l,cleanup
    cleanup,0,0,l,cleanup
    cleanup,1,1,l,cleanup
    cleanup,b,b,n,halt
    ```
    This encodes to (see the wiki definition above)
    `;DADDRDAA;DAADCDCCRDAA;DAADCCDCRDAA;DAADDLDAAA;DAAADCDCLDAAA;DAAADCCDCCLDAAA;DAAADDNDH`
