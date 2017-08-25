#!/usr/bin/python3 -u

import json
import signal
import sys
from tetrisGame import *

signal.alarm(3*60)

FIGURES_TO_THROW    = 10
GAMES_TO_SOLVE      = 100
TETRIS_FRAME_SIZE   = 10

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
""")
print("You could respond with(but json encoded):")
print("""
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
    flagFile = open("flag")
    flag = flagFile.read().strip()
    connection.sendall(flag.encode(encoding='UTF-8'))
