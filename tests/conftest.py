from dataclasses import dataclass

import pytest

from grafci.result_collector import ResultsCollector


@dataclass(init=True)
class TestReport:
    nodeid: str
    outcome: str
    longreprtext: str


@pytest.fixture
def test_results():
    reports = [
        TestReport('test_1', 'success', None),
        TestReport('test_2', 'fail', 'def text(): failed')
    ]

    collector = ResultsCollector()
    collector.reports = reports
    return collector
