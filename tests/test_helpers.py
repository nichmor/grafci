import socket
import pytest
from threading import Thread
from ci import helpers

PORT = 9999


def run_test_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(1)
    print('listening')
    conn, addr = server_socket.accept()
    print('accepted')
    data = conn.recv(1024)
    conn.sendall(data)
    conn.close()


def test_communicate():
    server_thread = Thread(target=run_test_socket_server, daemon=True)
    print('before run')
    server_thread.start()
    print('before communicate')
    response = helpers.communicate('localhost', PORT, 'test_data')
    assert  response == 'test_data'
    server_thread.join()