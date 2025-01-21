import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "extended_stays: mark tests related to extended stays"
    )
