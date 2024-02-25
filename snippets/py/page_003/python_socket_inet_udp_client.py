from socket import AF_INET, SOCK_DGRAM, socket

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("localhost", 6667))
while True:
    msg, addr = sock.recvfrom(
        8192
    )  # This is the amount of bytes to read at maximum
    print("Got message from %s: %s" % (addr, msg))
