"""
Pytest configuration file for network interruption tests.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "network_interruptions: marks tests that simulate network interruptions"
    )
