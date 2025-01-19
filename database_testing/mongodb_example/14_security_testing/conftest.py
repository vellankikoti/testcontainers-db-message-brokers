# conftest.py

import pytest

@pytest.fixture(scope="module")
def mock_password():
    """Fixture to provide a mock password for testing."""
    return "mockPassword123"
