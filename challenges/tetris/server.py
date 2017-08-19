#!/usr/bin/python3

import json
import socket
import sys
from tetrisGame import *


FIGURES_TO_THROW = 10


def initServer(port): 
    # Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port
    server_address = ('localhost', port)
    sock.bind(server_address)
    
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
            for i in range(100):
                tetrisFrame = TetrisFrame()
                tetrisGame = TetrisGame(tetrisFrame)
                tetrisFrameData = fillTetrisFrame(tetrisGame)
                
                frameDump = json.dumps(tetrisFrameData)
                connection.sendall(frameDump.encode(encoding='UTF-8'))
                
                data = connection.recv(520)
                dataDecoded = data.decode(encoding='UTF-8')
                matrix = json.loads(dataDecoded)

                print(checkTetrisFrame(tetrisGame, matrix))
        finally:
            # Clean up the connection
            connection.close()
