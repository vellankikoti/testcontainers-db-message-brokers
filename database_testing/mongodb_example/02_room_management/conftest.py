"""
conftest.py - Pytest Configuration for Room Management Tests

This module contains pytest configurations and shared fixtures for room management tests.
"""

def pytest_configure(config):
    """Register custom markers for room management tests."""
    config.addinivalue_line(
        "markers",
        "room_management: marks tests related to room management functionality"
    )
