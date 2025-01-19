"""
Configuration file for pytest with custom markers.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "performance: marks tests that measure database performance"
    )
