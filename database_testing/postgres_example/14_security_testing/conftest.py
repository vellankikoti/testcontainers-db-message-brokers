"""
Pytest configuration file for security tests.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "security: marks tests that verify application security"
    )
