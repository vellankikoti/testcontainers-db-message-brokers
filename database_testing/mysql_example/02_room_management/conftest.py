import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "room_management: mark tests related to room management"
    )
