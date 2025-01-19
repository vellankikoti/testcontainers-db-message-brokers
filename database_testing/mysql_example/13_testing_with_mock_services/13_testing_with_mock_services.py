"""
Testing with Mock Services Example

This script demonstrates how to test applications that interact with external services
using mock services to simulate different scenarios and responses.
"""

import pytest
import json
from unittest.mock import Mock, patch
from testcontainers.mysql import MySqlContainer
from sqlalchemy import create_engine, text
import requests
import time

# Constants
MYSQL_VERSION = "mysql:8.0"
MYSQL_ROOT_PASSWORD = "test"
DATABASE_NAME = "payment_service"

class PaymentGateway:
    """Simulates an external payment gateway service."""

    def __init__(self, api_key, base_url="https://api.payment-gateway.com"):
        self.api_key = api_key
        self.base_url = base_url

    def process_payment(self, amount, currency, card_details):
        """Process a payment through the payment gateway."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "amount": amount,
            "currency": currency,
            "card": card_details
        }

        response = requests.post(
            f"{self.base_url}/v1/payments",
            headers=headers,
            json=payload
        )
        return response.json()

class PaymentService:
    """Handles payment processing and database operations."""

    def __init__(self, db_engine, payment_gateway):
        self.engine = db_engine
        self.payment_gateway = payment_gateway
        self.setup_database()

    def setup_database(self):
        """Initialize the database schema."""
        with self.engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10, 2) NOT NULL,
                    currency VARCHAR(3) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    transaction_id VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            connection.commit()

    def process_payment(self, amount, currency, card_details):
        """Process a payment and store the result."""
        try:
            # Process payment through gateway
            result = self.payment_gateway.process_payment(amount, currency, card_details)

            # Store payment record
            with self.engine.begin() as connection:
                connection.execute(
                    text("""
                        INSERT INTO payments (amount, currency, status, transaction_id)
                        VALUES (:amount, :currency, :status, :transaction_id)
                    """),
                    {
                        "amount": amount,
                        "currency": currency,
                        "status": result.get("status", "failed"),
                        "transaction_id": result.get("transaction_id")
                    }
                )

            return result

        except Exception as e:
            # Log error and store failed payment
            with self.engine.begin() as connection:
                connection.execute(
                    text("""
                        INSERT INTO payments (amount, currency, status)
                        VALUES (:amount, :currency, 'error')
                    """),
                    {
                        "amount": amount,
                        "currency": currency
                    }
                )
            raise

class MockPaymentGateway:
    """Mock implementation of the payment gateway for testing."""

    def __init__(self, should_fail=False, delay=0):
        self.should_fail = should_fail
        self.delay = delay

    def process_payment(self, amount, currency, card_details):
        """Simulate payment processing with configurable behavior."""
        if self.delay:
            time.sleep(self.delay)

        if self.should_fail:
            raise requests.exceptions.RequestException("Payment gateway error")

        return {
            "status": "success",
            "transaction_id": "mock-txn-123",
            "amount": amount,
            "currency": currency
        }

@pytest.fixture(scope="function")
def mysql_container():
    """Fixture to provide a MySQL container."""
    container = MySqlContainer(MYSQL_VERSION)
    container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
    container.with_env("MYSQL_DATABASE", DATABASE_NAME)

    container.start()
    engine = create_engine(container.get_connection_url())

    yield engine

    engine.dispose()
    container.stop()

@pytest.mark.mock_services
def test_successful_payment(mysql_container):
    """Test successful payment processing with mock gateway."""
    # Setup
    mock_gateway = MockPaymentGateway()
    payment_service = PaymentService(mysql_container, mock_gateway)

    # Test data
    amount = 100.00
    currency = "USD"
    card_details = {
        "number": "4111111111111111",
        "expiry": "12/24",
        "cvv": "123"
    }

    # Process payment
    result = payment_service.process_payment(amount, currency, card_details)

    # Verify result
    assert result["status"] == "success"
    assert result["transaction_id"] == "mock-txn-123"

    # Verify database record
    with mysql_container.connect() as connection:
        payment_record = connection.execute(
            text("SELECT * FROM payments ORDER BY id DESC LIMIT 1")
        ).fetchone()

    assert payment_record.amount == amount
    assert payment_record.currency == currency
    assert payment_record.status == "success"

@pytest.mark.mock_services
def test_failed_payment(mysql_container):
    """Test payment processing when gateway fails."""
    # Setup
    mock_gateway = MockPaymentGateway(should_fail=True)
    payment_service = PaymentService(mysql_container, mock_gateway)

    # Test data
    amount = 100.00
    currency = "USD"
    card_details = {
        "number": "4111111111111111",
        "expiry": "12/24",
        "cvv": "123"
    }

    # Process payment and expect exception
    with pytest.raises(requests.exceptions.RequestException):
        payment_service.process_payment(amount, currency, card_details)

    # Verify error record in database
    with mysql_container.connect() as connection:
        payment_record = connection.execute(
            text("SELECT * FROM payments ORDER BY id DESC LIMIT 1")
        ).fetchone()

    assert payment_record.amount == amount
    assert payment_record.currency == currency
    assert payment_record.status == "error"

@pytest.mark.mock_services
def test_slow_payment_processing(mysql_container):
    """Test payment processing with delayed gateway response."""
    # Setup
    mock_gateway = MockPaymentGateway(delay=2)
    payment_service = PaymentService(mysql_container, mock_gateway)

    # Test data
    amount = 100.00
    currency = "USD"
    card_details = {
        "number": "4111111111111111",
        "expiry": "12/24",
        "cvv": "123"
    }

    # Process payment
    result = payment_service.process_payment(amount, currency, card_details)

    # Verify result
    assert result["status"] == "success"

    # Verify database record
    with mysql_container.connect() as connection:
        payment_record = connection.execute(
            text("SELECT * FROM payments ORDER BY id DESC LIMIT 1")
        ).fetchone()

    assert payment_record.status == "success"

def run_mock_services_test():
    """Run the mock services test directly."""
    print("\nStarting mock services test...")
    container = None
    engine = None

    try:
        # Setup container
        container = MySqlContainer(MYSQL_VERSION)
        container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        container.with_env("MYSQL_DATABASE", DATABASE_NAME)
        container.start()
        print("MySQL container started.")

        engine = create_engine(container.get_connection_url())

        # Run tests
        print("\nTesting successful payment...")
        test_successful_payment(engine)
        print("Successful payment test passed!")

        print("\nTesting failed payment...")
        test_failed_payment(engine)
        print("Failed payment test passed!")

        print("\nTesting slow payment processing...")
        test_slow_payment_processing(engine)
        print("Slow payment test passed!")

        print("\nAll tests completed successfully!")

    except Exception as e:
        print(f"\nTest failed: {e}")
        raise
    finally:
        print("\nCleaning up...")
        try:
            if engine:
                engine.dispose()
            if container:
                container.stop()
            print("Cleanup completed.")
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    run_mock_services_test()
