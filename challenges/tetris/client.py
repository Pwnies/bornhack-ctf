#!/usr/bin/python3

import json
import socket
import sys
from tetrisFrameSolver2 import *

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8083)

    sock.connect(server_address)

    blocks = findBlockPossibilities()
    try:
        while True:
            data = sock.recv(520)
            if not data:
                break
            dataDecoded = data.decode(encoding='UTF-8')
            
            if(dataDecoded[0] != '['):
                print(dataDecoded)
                break

            matrix = json.loads(dataDecoded)
            print(matrix)

            solution = findASolutionFromBlocks(matrix, blocks)
            print(solution)
            matrix = solutionToMatrix(solution)
            print(matrix)
            frameDump = json.dumps(matrix)
            
            sock.sendall(frameDump.encode(encoding='UTF-8'))
    finally:
        sock.close()
