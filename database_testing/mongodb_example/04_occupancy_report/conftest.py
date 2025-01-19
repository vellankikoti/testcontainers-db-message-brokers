"""
conftest.py - Pytest Configuration for Occupancy Report Tests

This module contains pytest configurations and shared fixtures for occupancy report tests.
"""

def pytest_configure(config):
    """Register custom markers for occupancy report tests."""
    config.addinivalue_line(
        "markers",
        "occupancy_report: marks tests related to occupancy reporting functionality"
    )
