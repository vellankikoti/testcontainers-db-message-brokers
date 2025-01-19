"""
Pytest configuration file for data migration testing.
"""

import pytest

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "migration: mark test as a migration test"
    )
