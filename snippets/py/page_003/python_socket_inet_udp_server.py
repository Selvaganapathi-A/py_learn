import time
from socket import AF_INET, SOCK_DGRAM, socket

import json5

s = socket(AF_INET, SOCK_DGRAM)

data = {
    "content-length": 1024,
    "data": "hi google",
    "from": "arizona, Missisipi",
    "user_code": [1, 4, 5, 2, 6, 2],
    "opcode": (1, 2, 4, 2, 1, 1, 2, 1),
}
msg = json5.dumps(data)

while True:
    s.sendto(msg.encode(), ("localhost", 1026))
    time.sleep(1)
