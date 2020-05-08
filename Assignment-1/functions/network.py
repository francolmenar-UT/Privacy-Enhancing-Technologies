import socket

def connect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def disconnect(sock):
    sock.close()


def send_message(message, sock):
    sock.sendall(message)

    data = sock.recv(1)

    return data
