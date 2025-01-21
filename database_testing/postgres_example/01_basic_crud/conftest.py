import pytest

def pytest_configure(config):
    """Configure pytest markers for the test suite.

    This configuration registers custom markers used across the test suite:
    - basic: Used for basic CRUD operation tests
    """
    config.addinivalue_line(
        "markers",
        "basic: mark test as a basic CRUD operation test case"
    )
