from unittest.mock import MagicMock, patch

from ci import helpers

# @patch('ci.helpers.socket.socket')
# def test_communicate(socket_mock: MagicMock):
#     socket_mock().recv.return_value = 'test_data'.encode('utf-8')
#     response = helpers.communicate('127.0.0.1', 9999, 'test_data')
#     assert response == 'test_data'

def test_build_results(test_results):
    results = helpers._build_results(test_results)
    for report in results.values():
        assert 'node' in report
        assert 'outcome' in report
        assert 'reason' in report


@patch('ci.helpers.ResultsCollector')
@patch('os.path.join')
@patch('ci.helpers.pytest.main')
def test_run_pytest_tests(pytest_mock, join_mock, result_mock):
    join_mock.return_value = 'test-folder/test-repo'
    helpers.run_pytest_tests('test_repo_folder')
    pytest_mock.assert_called_with(
        ['test-folder/test-repo'], plugins=[result_mock()])
