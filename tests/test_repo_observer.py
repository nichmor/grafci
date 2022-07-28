import argparse
import socket
import subprocess
from ci import repo_observer
import pytest
from unittest.mock import MagicMock, mock_open, patch



def test_parse_args():
    arg_string = ["--dispatcher-server", "localhost:8888" , "test_repo"]
    namespace = repo_observer.parse_args(arg_string)
    assert namespace.dispatcher_server == "localhost:8888"
    assert namespace.repo == "test_repo"

@patch("ci.repo_observer.subprocess.check_output")
def test_update_repository(mock_check_output):
    mock_check_output.return_value = True
    update_result = repo_observer.update_repository("test_repo")
    assert True == update_result

@patch("ci.repo_observer.subprocess.check_output", side_effect=subprocess.CalledProcessError(-1, "test_cmd"))
def test_update_repository_raise_exception(mock_check_output):
    with pytest.raises(SystemError) as system_error:
        repo_observer.update_repository("test_repo")
        assert "test_cmd" in system_error

@patch("ci.repo_observer.helpers.communicate")
def test_verify_dispatcher_status(communicate_mock):
    communicate_mock.return_value = "OK"
    assert "OK" == repo_observer.verify_dispatcher_status("localhost", 9999)

@patch("ci.repo_observer.helpers.communicate", side_effect=socket.error("system_error"))
def test_verify_dispatcher_status_raise_exception(communicate_mock):
    with pytest.raises(ConnectionError) as connection_error:
        repo_observer.verify_dispatcher_status("localhost", 9999)
        assert "system_error" in connection_error

@patch("ci.repo_observer.open", new_callable=mock_open, read_data='commit_1')
@patch("ci.repo_observer.helpers.communicate")
def test_dispatch_commit_for_test(mock_communicate, mock_open):
    mock_communicate.return_value = 'OK'
    repo_observer.dispatch_commit_for_test('localhost', 9999)
    mock_communicate.assert_called_with('localhost', 9999, 'dispatch:commit_1')

@patch("ci.repo_observer.open", new_callable=mock_open, read_data='commit_1')
@patch("ci.repo_observer.helpers.communicate")
def test_dispatch_commit_for_test_raise_exception(mock_communicate, mock_open):
    with pytest.raises(ConnectionError):
        mock_communicate.return_value = 'NOT_OK'
        repo_observer.dispatch_commit_for_test('localhost', 9999)

@patch("ci.repo_observer.os.path.isfile")
@patch("ci.repo_observer.dispatch_commit_for_test")
@patch("ci.repo_observer.verify_dispatcher_status")
@patch("ci.repo_observer.update_repository")
def test_poll(update_repository_mock, verify_dispatcher_status, dispatch_mock, is_file_mock):
    is_file_mock.return_value = True
    verify_dispatcher_status.return_value = 'OK'
    repo_observer._poll("localhost", "9999", "test_repo")

@patch("ci.repo_observer.os.path.isfile")
@patch("ci.repo_observer.update_repository")
def test_poll_no_commit(update_repository_mock, is_file_mock):
    is_file_mock.return_value = False
    repo_observer._poll("localhost", "9999", "test_repo")


@patch("ci.repo_observer.os.path.isfile")
@patch("ci.repo_observer.verify_dispatcher_status")
@patch("ci.repo_observer.update_repository")
def test_poll_raise_exception(update_repository_mock, verify_dispatcher_status,  is_file_mock):
    is_file_mock.return_value = True
    verify_dispatcher_status.return_value = 'NOT_OK'
    with pytest.raises(ConnectionError):
        repo_observer._poll("localhost", "9999", "test_repo")