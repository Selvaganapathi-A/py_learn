import socket


def createServer(*args, **kwargs):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("127.0.0.1", 8001))
        server.listen(5)
        while True:
            connection, address = server.accept()
            print(address)
            clientData = connection.recv(4096)
            print(clientData.decode())
            data = "HTTP/6.1 404 Ok\r\n"
            data += "content-type:text/html charset:utf-8\r\n"
            data += "\r\n\r\n"
            data += '<html><body><h2 style="color:red">Hi</h2><p>Google</p></body></html>\r\n'
            connection.send(data.encode())
            connection.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt as ki:
        print("Server power down...")
    except Exception as e:
        raise TimeoutError("Max time reached as per my boss") from e


createServer()
