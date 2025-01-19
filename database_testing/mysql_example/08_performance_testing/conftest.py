"""
Pytest configuration file for performance testing
"""

import pytest

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "performance: mark test as a performance test"
    )
