"""
Network Interruptions Test Suite

This module tests database behavior under various network conditions:
- Connection timeouts
- Network latency
- Connection drops
- Reconnection attempts
"""

import pytest
import time
import random
from contextlib import contextmanager
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError


class UnstablePostgresContainer(PostgresContainer):
    """Custom container class that simulates network instability."""

    def __init__(self, image="postgres:15.3", failure_rate=0.3, max_latency=2):
        super().__init__(image)
        self.failure_rate = failure_rate
        self.max_latency = max_latency

    @contextmanager
    def simulate_network_issues(self):
        """Simulate various network problems."""
        if random.random() < self.failure_rate:
            issue_type = random.choice(['latency', 'timeout', 'disconnect'])

            if issue_type == 'latency':
                latency = random.uniform(0, self.max_latency)
                time.sleep(latency)
                yield
            elif issue_type == 'timeout':
                time.sleep(5)  # Simulate a timeout
                raise OperationalError("Connection timed out", None, None)
            else:  # disconnect
                raise OperationalError("Connection reset by peer", None, None)
        else:
            yield


def setup_database(connection):
    """Initialize the database schema."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
    connection.commit()


def insert_with_retry(connection, amount, max_retries=3):
    """Insert a transaction with retry logic."""
    retries = 0
    while retries < max_retries:
        try:
            connection.execute(
                text("INSERT INTO transactions (amount, status) VALUES (:amount, 'pending')"),
                {"amount": amount}
            )
            connection.commit()
            return True
        except SQLAlchemyError as e:
            retries += 1
            print(f"Retry {retries}/{max_retries} due to: {str(e)}")
            time.sleep(1)  # Wait before retrying

    return False


@pytest.mark.network_interruptions
def test_database_resilience():
    """Test database operations under unstable network conditions."""
    # Create container with custom parameters
    container = UnstablePostgresContainer(
        image="postgres:15.3",
        failure_rate=0.3,
        max_latency=2
    )

    with container:
        engine = create_engine(container.get_connection_url())
        successful_transactions = 0
        failed_transactions = 0

        # Initial setup
        with engine.connect() as connection:
            setup_database(connection)

        # Perform multiple transactions under unstable conditions
        for i in range(10):
            with engine.connect() as connection:
                try:
                    with container.simulate_network_issues():
                        amount = random.uniform(10, 1000)
                        if insert_with_retry(connection, amount):
                            successful_transactions += 1
                            print(f"✅ Transaction {i+1} successful: ${amount:.2f}")
                        else:
                            failed_transactions += 1
                            print(f"❌ Transaction {i+1} failed after retries")
                except OperationalError as e:
                    failed_transactions += 1
                    print(f"❌ Transaction {i+1} failed: {str(e)}")

        # Final statistics
        total_transactions = successful_transactions + failed_transactions
        success_rate = (successful_transactions / total_transactions) * 100

        print(f"\n📊 Test Statistics:")
        print(f"Total Transactions: {total_transactions}")
        print(f"Successful: {successful_transactions}")
        print(f"Failed: {failed_transactions}")
        print(f"Success Rate: {success_rate:.1f}%")

        # Verify minimum success rate
        assert success_rate >= 60, f"Success rate ({success_rate:.1f}%) below minimum threshold (60%)"
        print("\n✅ Database resilience test completed successfully!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
