import pytest

def pytest_configure(config):
    """Configure pytest markers for the failure simulation test suite."""
    config.addinivalue_line(
        "markers",
        "failures: mark test as a failure simulation test case"
    )
