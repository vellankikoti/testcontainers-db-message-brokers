"""
Network Interruptions Testing Example

This script tests database operations under simulated network interruptions
using custom container configurations and network manipulation.
"""

import pytest
import time
import random
from sqlalchemy import create_engine, text
from testcontainers.mysql import MySqlContainer
from contextlib import contextmanager

# Constants
MYSQL_VERSION = "mysql:8.0"
DATABASE_NAME = "network_test"
MYSQL_ROOT_PASSWORD = "test"

class UnstableMySQLContainer(MySqlContainer):
    """Custom MySQL container that simulates network instability."""

    def __init__(self, image="mysql:8.0", failure_rate=0.3, max_delay=2):
        super().__init__(image)
        self.failure_rate = failure_rate
        self.max_delay = max_delay
        # Set required MySQL environment variables
        self.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        self.with_env("MYSQL_DATABASE", DATABASE_NAME)

    def simulate_network_issue(self):
        """Simulate network issues with random delays and failures."""
        if random.random() < self.failure_rate:
            delay = random.uniform(0, self.max_delay)
            print(f"\nSimulating network delay of {delay:.2f} seconds...")
            time.sleep(delay)
            if random.random() < 0.5:
                raise ConnectionError("Simulated network interruption")

def wait_for_mysql_ready(engine, max_retries=10, retry_interval=2):
    """Wait for the MySQL database to be ready."""
    print("\nWaiting for MySQL to be ready...")
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("MySQL is ready!")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet. Retrying...")
            time.sleep(retry_interval)
    raise RuntimeError("MySQL did not become ready in time.")

@pytest.fixture(scope="function")
def unstable_mysql():
    """Fixture to provide an unstable MySQL container."""
    container = UnstableMySQLContainer()
    try:
        container.start()
        engine = create_engine(container.get_connection_url())
        wait_for_mysql_ready(engine)
        setup_database(engine)
        yield container, engine
    finally:
        if 'engine' in locals():
            engine.dispose()
        container.stop()

def setup_database(engine):
    """Initialize the database schema."""
    print("\nSetting up database schema...")
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                CHECK (balance >= 0)
            );
        """))
        connection.commit()

        # Insert sample data
        connection.execute(text("""
            INSERT INTO accounts (name, balance) VALUES
            ('Alice', 1000.00),
            ('Bob', 500.00);
        """))
        connection.commit()
        print("Database schema and sample data created.")

def transfer_funds(container, engine, from_account, to_account, amount, max_retries=3):
    """Transfer funds between accounts with retry logic."""
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Simulate potential network issues
            container.simulate_network_issue()

            with engine.begin() as connection:
                # Check sufficient funds
                result = connection.execute(
                    text("SELECT balance FROM accounts WHERE name = :name"),
                    {"name": from_account}
                ).fetchone()

                if not result or result[0] < amount:
                    raise ValueError("Insufficient funds")

                # Perform transfer
                connection.execute(
                    text("""
                        UPDATE accounts 
                        SET balance = balance - :amount 
                        WHERE name = :from_name
                    """),
                    {"amount": amount, "from_name": from_account}
                )

                connection.execute(
                    text("""
                        UPDATE accounts 
                        SET balance = balance + :amount 
                        WHERE name = :to_name
                    """),
                    {"amount": amount, "to_name": to_account}
                )

                print(f"\nTransferred ${amount:.2f} from {from_account} to {to_account}")
                return True

        except Exception as e:
            retry_count += 1
            print(f"\nTransfer attempt {retry_count} failed: {str(e)}")
            if retry_count >= max_retries:
                print("Max retries reached. Transfer failed.")
                raise

def get_balance(engine, account_name):
    """Get the current balance for an account."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT balance FROM accounts WHERE name = :name"),
            {"name": account_name}
        ).fetchone()
        return result[0] if result else None

@pytest.mark.network
def test_fund_transfer_with_interruptions(unstable_mysql):
    """Test fund transfers under network interruptions."""
    container, engine = unstable_mysql

    # Initial balances
    alice_initial = get_balance(engine, "Alice")
    bob_initial = get_balance(engine, "Bob")

    print(f"\nInitial balances: Alice=${alice_initial:.2f}, Bob=${bob_initial:.2f}")

    # Perform transfer with potential interruptions
    transfer_amount = 100.00
    transfer_funds(container, engine, "Alice", "Bob", transfer_amount)

    # Verify final balances
    alice_final = get_balance(engine, "Alice")
    bob_final = get_balance(engine, "Bob")

    print(f"\nFinal balances: Alice=${alice_final:.2f}, Bob=${bob_final:.2f}")

    # Verify the transfer was successful
    assert alice_final == alice_initial - transfer_amount
    assert bob_final == bob_initial + transfer_amount

def run_network_test():
    """Run the network interruption test directly."""
    print("\nStarting network interruption test...")
    container = None
    engine = None
    try:
        container = UnstableMySQLContainer()
        container.start()
        print("MySQL container started.")

        engine = create_engine(container.get_connection_url())
        wait_for_mysql_ready(engine)
        setup_database(engine)

        # Initial balances
        alice_initial = get_balance(engine, "Alice")
        bob_initial = get_balance(engine, "Bob")

        print(f"\nInitial balances: Alice=${alice_initial:.2f}, Bob=${bob_initial:.2f}")

        # Perform transfer with potential interruptions
        transfer_amount = 100.00
        transfer_funds(container, engine, "Alice", "Bob", transfer_amount)

        # Verify final balances
        alice_final = get_balance(engine, "Alice")
        bob_final = get_balance(engine, "Bob")

        print(f"\nFinal balances: Alice=${alice_final:.2f}, Bob=${bob_final:.2f}")

        print("\nTest completed successfully!")

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
    run_network_test()
