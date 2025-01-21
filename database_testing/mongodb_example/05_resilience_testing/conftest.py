"""
conftest.py - Pytest Configuration for Extended Stay Tests

This module contains pytest configurations and shared fixtures for extended stay tests.
"""

def pytest_configure(config):
    """Register custom markers for extended stay tests."""
    config.addinivalue_line(
        "markers",
        "extended_stays: marks tests related to extended stay functionality"
    )
