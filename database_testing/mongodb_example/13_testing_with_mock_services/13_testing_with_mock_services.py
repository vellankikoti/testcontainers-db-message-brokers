"""
13_testing_with_mock_services.py - Testing with Mock Services

This example demonstrates how to test interactions with an external payment service using a mock service.
"""

import pytest
import requests
from unittest.mock import patch

# Function to process a payment
def process_payment(payment_info):
    """Process a payment by sending a request to the payment service."""
    response = requests.post("http://mock-payment-service.com/api/pay", json=payment_info)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Payment processing failed.")

# Test function for successful payment
def test_process_payment_success():
    payment_info = {
        "amount": 100.0,
        "currency": "USD",
        "source": "card_1234567890"
    }

    # Mock the requests.post method
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success", "transaction_id": "txn_12345"}

        result = process_payment(payment_info)

        assert result["status"] == "success"
        assert result["transaction_id"] == "txn_12345"
        mock_post.assert_called_once_with("http://mock-payment-service.com/api/pay", json=payment_info)

# Test function for failed payment
def test_process_payment_failure():
    payment_info = {
        "amount": 100.0,
        "currency": "USD",
        "source": "card_1234567890"
    }

    # Mock the requests.post method
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 400  # Simulate a failure response

        with pytest.raises(Exception, match="Payment processing failed."):
            process_payment(payment_info)

        mock_post.assert_called_once_with("http://mock-payment-service.com/api/pay", json=payment_info)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
