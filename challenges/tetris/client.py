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
            try:
                data = sock.recv(320)
                if not data:
                    break
                dataDecoded = data.decode(encoding='UTF-8')
                matrix = json.loads(dataDecoded)
                for row in matrix:
                    print(row)

                sock.sendall(data)
            finally:
                break
    finally:
        sock.close()
