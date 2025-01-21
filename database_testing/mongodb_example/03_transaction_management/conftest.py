"""
conftest.py - Pytest Configuration for Reservation Management Tests

This module contains pytest configurations and shared fixtures for reservation management tests.
"""

def pytest_configure(config):
    """Register custom markers for reservation management tests."""
    config.addinivalue_line(
        "markers",
        "reservation_management: marks tests related to reservation management functionality"
    )
