import pytest

def pytest_configure(config):
    """Configure pytest markers for the room management test suite."""
    config.addinivalue_line(
        "markers",
        "rooms: mark test as a room management test case"
    )
