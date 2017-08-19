#!/usr/bin/python3

import json
import socket
import sys

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8083)

    sock.connect(server_address)

    try:
        while True:
            data = sock.recv(520)
            if not data:
                break
            dataDecoded = data.decode(encoding='UTF-8')
            matrix = json.loads(dataDecoded)

            sock.sendall(data)
    finally:
        sock.close()
