import socket

def communicate(host, port, request: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request.encode('utf-8'))
    response = s.recv(1024)
    s.close()
    return response.decode('utf-8')