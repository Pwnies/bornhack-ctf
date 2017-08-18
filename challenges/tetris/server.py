#!/usr/bin/python3

import json
import socket
import sys
from tetrisGame import *


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
    for i in range(len(tetrisGame.figures)):
        tetrisGame.throwFigure()

    return tetrisGame.frame.frameData


def checkTetrisFrame(tetrisGame, clientMatrix):
    xoutFrame = copy.deepcopy(tetrisGame.frame)
    xout = xoutFrame.getXout()
    checker = CheckTetrisGame(xout, clientMatrix, tetrisGame.figures)
    shapes = checker.findShapes()
    
    match = True
    for shapeNo, shape in shapes.items():
        figureNo = checker.shapeNoToFigNo[shapeNo]
        shapeMatrix = checker.createMatrixFromFigure(shape)
        figuresInShape = checker.extractFigures(shapeMatrix, figureNo)
        if not figuresInShape:
            match = False

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
                print("TOSEND")
                print(type(frameDump))
                connection.sendall(frameDump.encode(encoding='UTF-8'))
                
                data = connection.recv(320)
                dataDecoded = data.decode(encoding='UTF-8')
                print(dataDecoded)
                matrix = json.loads(dataDecoded)

                print(checkTetrisFrame(tetrisGame, matrix))
                print("RUN THROUGH!")
        finally:
            # Clean up the connection
            connection.close()
