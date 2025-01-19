"""
conftest.py - Pytest Configuration for Simulating Failures

This module contains pytest configurations and shared fixtures for failure simulation tests.
"""

def pytest_configure(config):
    """Register custom markers for failure simulation tests."""
    config.addinivalue_line(
        "markers",
        "simulating_failures: marks tests related to simulating database failures"
    )
