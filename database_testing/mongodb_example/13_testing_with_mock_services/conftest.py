# conftest.py
import pytest

@pytest.fixture(scope="module")
def payment_service_url():
    """Fixture to provide the mock payment service URL."""
    return "http://mock-payment-service.com/api/pay"

# You can add more fixtures here as needed for other tests or configurations.
