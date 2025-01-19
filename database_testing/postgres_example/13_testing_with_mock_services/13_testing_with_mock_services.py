"""
Testing with Mock Services

This module tests the interaction with an external payment service using a mock service.
The tests ensure that:
- The application correctly handles successful payment responses.
- The application correctly handles failed payment responses.
"""

import pytest
import requests
from unittest.mock import patch


class PaymentService:
    """A simple payment service client."""

    def __init__(self, base_url):
        self.base_url = base_url

    def process_payment(self, user_id, amount):
        """Send a payment request to the external service."""
        response = requests.post(f"{self.base_url}/process_payment", json={"user_id": user_id, "amount": amount})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


@pytest.mark.mock_services
def test_payment_service_success():
    """Test successful payment processing."""
    with patch("requests.post") as mock_post:
        # Mock the response for a successful payment
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success", "transaction_id": "12345"}

        # Initialize the payment service
        service = PaymentService("http://mock-service.com")

        # Call the process_payment method
        response = service.process_payment(user_id=1, amount=100.0)

        # Assertions
        assert response["status"] == "success"
        assert response["transaction_id"] == "12345"
        print("✅ Payment service success test passed")


@pytest.mark.mock_services
def test_payment_service_failure():
    """Test failed payment processing."""
    with patch("requests.post") as mock_post:
        # Mock the response for a failed payment
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"status": "failure", "error": "Insufficient funds"}

        # Initialize the payment service
        service = PaymentService("http://mock-service.com")

        # Call the process_payment method and handle the exception
        try:
            service.process_payment(user_id=1, amount=1000.0)
        except requests.exceptions.HTTPError as e:
            # Assertions
            assert "400 Client Error" in str(e)
            print("✅ Payment service failure test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
