"""
Pytest Configuration for Multiple Containers Example
"""

import pytest

def pytest_configure(config):
    """Register custom markers for pytest."""
    config.addinivalue_line("markers", "integration: mark a test as an integration test.")
