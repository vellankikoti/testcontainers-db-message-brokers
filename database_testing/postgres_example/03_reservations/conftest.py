import pytest

def pytest_configure(config):
    """Configure pytest markers for the reservation system test suite."""
    config.addinivalue_line(
        "markers",
        "reservations: mark test as a reservation system test case"
    )
