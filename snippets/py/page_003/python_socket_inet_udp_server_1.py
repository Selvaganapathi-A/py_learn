import pprint
import socket

import json5

def createServer(*args, **kwargs):
    myserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    myserver.bind(("localhost", 30000))
    while True:
        pprint.pprint(json5.loads(myserver.recv(1024).decode()))


createServer()
