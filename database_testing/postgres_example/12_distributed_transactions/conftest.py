"""
Pytest configuration file for distributed transaction tests.
"""

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "distributed_transactions: marks tests that verify distributed transactions"
    )
