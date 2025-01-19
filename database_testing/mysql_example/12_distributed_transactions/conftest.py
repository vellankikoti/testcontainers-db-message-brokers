"""
Pytest configuration for distributed transaction testing.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "distributed: mark test as a distributed transaction test"
    )
