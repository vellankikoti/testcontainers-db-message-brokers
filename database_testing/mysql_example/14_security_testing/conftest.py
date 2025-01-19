"""
Pytest configuration for security testing.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "security: mark test as a security test"
    )
