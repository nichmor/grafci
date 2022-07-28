import socket
import time
from threading import Thread
from unittest.mock import MagicMock, patch
from ci import helpers


@patch('ci.helpers.socket.socket')
def test_communicate(socket_mock: MagicMock):
    socket_mock().recv.return_value = 'test_data'.encode('utf-8')
    response = helpers.communicate('127.0.0.1', 9999, 'test_data')
    assert response == 'test_data'