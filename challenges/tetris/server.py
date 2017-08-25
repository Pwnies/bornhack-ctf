#!/usr/bin/python3

import calendar
import json
import socket
import sys
import time
from tetrisGame import *


FIGURES_TO_THROW    = 6
GAMES_TO_SOLVE      = 100
TETRIS_FRAME_SIZE   = 8


def initServer(port): 
    # Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port
    HOST, PORT = ('0.0.0.0', port)
    sock.bind((HOST, PORT))
    print("Running on " + HOST + ':' + str(PORT))
    
    # Listen for incoming connections
    sock.listen(1)

    return sock


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
        print(1)
        print(matrix)
        return False
    elif(len(matrix) != TETRIS_FRAME_SIZE):
        print(2)
        print(len(matrix))
        return False

    FIRST_ASCII = ord('a')
    LAST_ASCII = FIRST_ASCII + FIGURES_TO_THROW - 1
    ZERO = ord('0')

    for row in range(TETRIS_FRAME_SIZE):
        if(len(matrix[row]) != TETRIS_FRAME_SIZE):
            print(3)
            print(len(matrix[row]))
            return False
        for column in range(TETRIS_FRAME_SIZE):
            if(type(matrix[row][column]) != str or len(matrix[row][column]) != 1):
                print(4)
                print(type(matrix[row][column]))
                print(len(matrix[row][column]))
                return False
            curAscii = ord(matrix[row][column])
            if(curAscii == ZERO):
                continue
            if(curAscii < FIRST_ASCII or curAscii > LAST_ASCII):
                print(curAscii)
                return False

    return True


def checkTetrisFrame(tetrisGame, clientMatrix):
    xoutFrame = copy.deepcopy(tetrisGame.frame)
    xout = xoutFrame.getXout()
    checker = CheckTetrisGame(xout, clientMatrix, tetrisGame.figures)
    figures = checker.findFigures()

    match = False

    if(len(figures) == FIGURES_TO_THROW):
        match = True

    return match


if __name__ == '__main__':
    sock = initServer(8083)

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        
        try:
            gamesSolved = 0
            startTime = calendar.timegm(time.gmtime())
            maxAllowedTimeUseSec = 3*60

            for i in range(GAMES_TO_SOLVE):
                curTime = calendar.timegm(time.gmtime())
                if (curTime - startTime > maxAllowedTimeUseSec):
                    print("Time limit exceeded")
                    break

                tetrisFrame = TetrisFrame()
                tetrisGame = TetrisGame(tetrisFrame)
                tetrisFrameData = fillTetrisFrame(tetrisGame)
                print(tetrisFrameData)

                frameDump = json.dumps(tetrisFrameData)
                connection.sendall(frameDump.encode(encoding='UTF-8'))
                
                data = connection.recv(520)
                dataDecoded = data.decode(encoding='UTF-8')
                matrix = json.loads(dataDecoded)

                print(matrix)
                if not validateInput(matrix):
                    print(str(i) + " could not validate")
                    break

                if(checkTetrisFrame(tetrisGame, matrix)):
                    gamesSolved += 1
                    print(gamesSolved)

            if(gamesSolved == GAMES_TO_SOLVE):
                # send flag
                flagFile = open("flag")
                flag = flagFile.read().strip()
                connection.sendall(flag.encode(encoding='UTF-8'))
        finally:
            # Clean up the connection
            connection.close()
