from unittest.mock import patch

from grafci import pytest_helpers


def test_build_results(test_results):
    results = pytest_helpers._build_results(test_results)
    for report in results.values():
        assert 'node' in report
        assert 'outcome' in report
        assert 'reason' in report


@patch('grafci.pytest_helpers.ResultsCollector')
@patch('os.path.join')
@patch('grafci.pytest_helpers.pytest.main')
def test_run_pytest_tests(pytest_mock, join_mock, result_mock):
    join_mock.return_value = 'test-folder/test-repo'
    pytest_helpers.run_pytest_tests('test_repo_folder')
    pytest_mock.assert_called_with(
        ['test-folder/test-repo'], plugins=[result_mock()])
