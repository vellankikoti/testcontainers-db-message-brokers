import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "reservations: mark tests related to reservations"
    )
