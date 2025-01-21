"""
Pytest configuration file for MySQL testing examples.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "basic: mark test as a basic MySQL operation test"
    )
