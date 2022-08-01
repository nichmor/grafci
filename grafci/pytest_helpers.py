import os

import pytest

from grafci.result_collector import ResultsCollector


def run_pytest_tests(repo_folder) -> dict:
    collector = ResultsCollector()
    tests_path = os.path.join(repo_folder, 'tests')
    pytest.main([tests_path], plugins=[collector])
    return _build_results(collector)


def _build_results(collector: ResultsCollector) -> dict[str, dict]:
    test_results = {}
    for report in collector.reports:
        report_dict = {
            'node': report.nodeid,
            'outcome': report.outcome,
            'reason': report.longreprtext if report.longreprtext else None,
        }
        test_results[report.nodeid] = report_dict

    return test_results
