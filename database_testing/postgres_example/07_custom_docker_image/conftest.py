"""
Configuration file for pytest with custom markers.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "custom_docker: marks tests that use custom Docker images"
    )
