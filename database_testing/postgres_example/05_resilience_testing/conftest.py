import pytest

def pytest_configure(config):
    """Configure pytest markers for the extended stays test suite."""
    config.addinivalue_line(
        "markers",
        "extended_stays: mark test as an extended stays test case"
    )
