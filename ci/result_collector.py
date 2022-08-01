import pytest


class ResultsCollector(object):  # pragma: no cover
    """Plugin for collecting test results."""

    def __init__(self):
        self.reports = []

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):  # noqa: WPS110
        outcome = yield
        report = outcome.get_result()
        if report.when == 'call':
            self.reports.append(report)
