"""
Pytest configuration for network interruption testing.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "network: mark test as a network interruption test"
    )
