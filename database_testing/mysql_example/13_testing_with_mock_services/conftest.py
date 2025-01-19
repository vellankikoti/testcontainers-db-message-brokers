"""
Pytest configuration for mock services testing.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "mock_services: mark test as a mock services test"
    )
