#!/usr/bin/python3 -u

import json
import signal
import sys
from tetrisGame import *

signal.alarm(3*60)

FIGURES_TO_THROW    = 6
GAMES_TO_SOLVE      = 100
TETRIS_FRAME_SIZE   = 8

def fillTetrisFrame(tetrisGame):
    for i in range(FIGURES_TO_THROW):
        tetrisGame.throwFigure()

    return tetrisGame.frame.getXout()


def validateInput(matrix):
    """
    Validate that matrix is a multidimentional array (TETRIS_FRAME_SIZE X TETRIS_FRAME_SIZE),
    and that all elements are ascii charachters (specifically the FIGURES_TO_THROW first lowercase lettes)
    """

    if(type(matrix) != list):
        return False
    elif(len(matrix) != TETRIS_FRAME_SIZE):
        return False

    FIRST_ASCII = ord('a')
    LAST_ASCII = FIRST_ASCII + FIGURES_TO_THROW - 1
    ZERO = ord('0')

    for row in range(TETRIS_FRAME_SIZE):
        if(len(matrix[row]) != TETRIS_FRAME_SIZE):
            return False
        for column in range(TETRIS_FRAME_SIZE):
            if(type(matrix[row][column]) != str or len(matrix[row][column]) != 1):
                return False
            curAscii = ord(matrix[row][column])
            if(curAscii == ZERO):
                continue
            if(curAscii < FIRST_ASCII or curAscii > LAST_ASCII):
                return False

    return True


def checkTetrisFrame(tetrisGame, clientMatrix):
    xoutFrame = copy.deepcopy(tetrisGame.frame)
    xout = xoutFrame.getXout()
    checker = CheckTetrisGame(xout, clientMatrix, tetrisGame.figures)
    figures = checker.findFigures()

    return len(figures) == FIGURES_TO_THROW

print("Welcome to our tetris coloring game!")
print("We send you some tetris game like(but json encoded):")
print("""
00000000
00000000
00000000
000X0000
X00XX000
XXX0XX00
XXXXXXXX
XXXXX0XX
""")
print("You could respond with(but json encoded):")
print("""
00000000
00000000
00000000
000e0000
f00ee000
fff0ed00
ccadddbb
ccaaa0bb
""")
print("Lets play:")

for i in range(GAMES_TO_SOLVE):
    tetrisFrame = TetrisFrame()
    tetrisGame = TetrisGame(tetrisFrame)
    tetrisFrameData = fillTetrisFrame(tetrisGame)

    json.dump(tetrisFrameData, sys.stdout)
    sys.stdout.flush()
    
    matrix = json.load(sys.stdin)

    if not validateInput(matrix):
        print(str(i) + " could not validate")
        break

    if(checkTetrisFrame(tetrisGame, matrix)):
        break
else:
    # send flag
    with open("flag") as flag:
        print(flag.read().strip())
