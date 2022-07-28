import subprocess
import unittest
from ci import repo_observer
import pytest
from unittest.mock import MagicMock, patch



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

