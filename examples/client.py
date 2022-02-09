#!/usr/bin/env python3

import socket
import json
import pickle
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b'Hello, world')
    data = s.recv(2578)
    #s.send(b'abc')
    #data = data.decode("utf-8")
    #data = json.loads(data)
    data = pickle.loads(data)
#print('Received', repr(data))
#print(data["_map"])
print(data.actions["movetopick"])