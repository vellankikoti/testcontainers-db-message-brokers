import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "simulating_failures: mark tests related to simulating database failures"
    )
