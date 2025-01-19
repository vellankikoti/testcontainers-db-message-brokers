"""
Pytest configuration file for mock services tests.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "mock_services: marks tests that verify interactions with mock services"
    )
