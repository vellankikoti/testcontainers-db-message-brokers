"""
Configuration file for pytest with custom markers.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "multiple_containers: marks tests that involve multiple containers"
    )
