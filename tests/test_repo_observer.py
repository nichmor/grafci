import subprocess
from unittest.mock import mock_open, patch

import pytest

from grafci import repo_observer


def test_parse_args():
    arg_string = ['test_repo']
    namespace = repo_observer.parse_args(arg_string)
    assert namespace.repo == 'test_repo'


@patch('grafci.repo_observer.subprocess.check_output')
def test_update_repository(mock_check_output):
    mock_check_output.return_value = True
    update_result = repo_observer.update_repository('test_repo')
    assert update_result


@patch('grafci.repo_observer.subprocess.check_output', side_effect=subprocess.CalledProcessError(-1, 'test_cmd'))
def test_update_repository_raise_exception(mock_check_output):
    with pytest.raises(SystemError) as system_error:
        repo_observer.update_repository('test_repo')
        assert 'test_cmd' in system_error


@patch('grafci.repo_observer.open', new_callable=mock_open, read_data='commit_1')
@patch('grafci.repo_observer.run_tests')
def test_dispatch_commit_for_test(mock_run_tests, mock_open):
    repo_observer.dispatch_commit_for_test('test_repo_folder')
    mock_run_tests.assert_called_with('commit_1', 'test_repo_folder')


@patch('grafci.repo_observer.os.path.isfile')
@patch('grafci.repo_observer.dispatch_commit_for_test')
@patch('grafci.repo_observer.update_repository')
def test_poll(update_repository_mock, dispatch_mock, is_file_mock):
    is_file_mock.return_value = True
    repo_observer._poll('test_repo')


@patch('grafci.repo_observer.os.path.isfile')
@patch('grafci.repo_observer.update_repository')
def test_poll_no_commit(update_repository_mock, is_file_mock):
    is_file_mock.return_value = False
    repo_observer._poll('test_repo')


@patch('grafci.repo_observer.json.dump')
@patch('grafci.repo_observer.open', new_callable=mock_open)
@patch('grafci.repo_observer.os.makedirs')
@patch('grafci.repo_observer.pytest_helpers.run_pytest_tests')
@patch('grafci.repo_observer.subprocess.check_output')
def test_run_tests(
    _,
    run_pytest_mock,
    make_dir_mock,
    open_mock,
    dump_mock,
    test_results
):
    run_pytest_mock.return_value = test_results
    repo_observer.run_tests('commit_1', 'test_folder')
    assert make_dir_mock.called
    assert open_mock.called
    assert dump_mock.called
