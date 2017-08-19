#!/usr/bin/python3

import calendar
import json
import socket
import sys
import time
from tetrisGame import *


FIGURES_TO_THROW    = 10
GAMES_TO_SOLVE      = 100


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

    return tetrisGame.frame.frameData


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
                    break

                tetrisFrame = TetrisFrame()
                tetrisGame = TetrisGame(tetrisFrame)
                tetrisFrameData = fillTetrisFrame(tetrisGame)
                
                # xout frame

                frameDump = json.dumps(tetrisFrameData)
                connection.sendall(frameDump.encode(encoding='UTF-8'))
                
                data = connection.recv(520)
                dataDecoded = data.decode(encoding='UTF-8')
                matrix = json.loads(dataDecoded)

                if(checkTetrisFrame(tetrisGame, matrix)):
                    gamesSolved += 1

            if(gamesSolved == GAMES_TO_SOLVE):
                # send flag
                flagFile = open("flag")
                flag = flagFile.read().strip()
                connection.sendall(flag.encode(encoding='UTF-8'))
        finally:
            # Clean up the connection
            connection.close()
