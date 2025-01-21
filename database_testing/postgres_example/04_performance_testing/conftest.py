import pytest

def pytest_configure(config):
    """Configure pytest markers for the occupancy report test suite."""
    config.addinivalue_line(
        "markers",
        "occupancy: mark test as an occupancy report test case"
    )
