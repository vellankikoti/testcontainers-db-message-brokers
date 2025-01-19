"""
Configuration file for pytest with custom markers.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "migration: marks tests that verify database migrations"
    )
