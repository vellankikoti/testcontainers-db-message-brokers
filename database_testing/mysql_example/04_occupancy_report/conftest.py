import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "occupancy_report: mark tests related to occupancy reports"
    )
