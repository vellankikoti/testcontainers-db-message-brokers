"""
Simulating Failures Test Suite

This module tests the system's ability to handle database failures, including:
- Connection errors
- Query execution errors
- Transaction rollbacks
"""

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError

# Constants
POSTGRES_VERSION = "postgres:15.3"

def setup_database(connection):
    """Initialize the database schema with a sample table."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            description TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status TEXT DEFAULT 'pending'
        );
    """))
    connection.commit()

def insert_sample_data(connection):
    """Insert sample transaction data."""
    connection.execute(text("""
        INSERT INTO transactions (description, amount, status) VALUES
        ('Payment A', 100.00, 'completed'),
        ('Payment B', 200.00, 'pending'),
        ('Payment C', 300.00, 'failed');
    """))
    connection.commit()

def simulate_query_failure(connection):
    """Simulate a query failure by executing invalid SQL."""
    try:
        connection.execute(text("SELECT * FROM non_existent_table;"))
        return False
    except ProgrammingError as e:
        print(f"Query failed as expected: {e}")
        return True

def verify_no_payment_d(connection):
    """Verify that Payment D was not inserted."""
    result = connection.execute(text(
        "SELECT COUNT(*) FROM transactions WHERE description = 'Payment D';"
    )).scalar()
    return result == 0

def simulate_transaction_failure(connection):
    """Simulate a transaction failure and rollback."""
    connection.commit()  # Ensure we're starting fresh

    try:
        # Execute the insert
        connection.execute(text("""
            INSERT INTO transactions (description, amount, status) 
            VALUES ('Payment D', 400.00, 'pending');
        """))

        # Simulate a failure
        raise RuntimeError("Simulated transaction failure")

    except RuntimeError as e:
        print(f"Transaction failed as expected: {e}")
        connection.rollback()
        # Verify the rollback was successful
        return verify_no_payment_d(connection)

    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()
        return False

@pytest.mark.failures
def test_simulating_failures():
    """Test the system's ability to handle simulated failures."""
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as connection:
            # Setup and insert sample data
            setup_database(connection)
            insert_sample_data(connection)

            # Test 1: Simulate query failure
            query_failed = simulate_query_failure(connection)
            assert query_failed, "Query should have failed"

            # Test 2: Simulate transaction failure
            transaction_rolled_back = simulate_transaction_failure(connection)
            assert transaction_rolled_back, "Transaction should have been rolled back"

            # Final verification
            assert verify_no_payment_d(connection), "Payment D should not exist in the database"

            print("\n✅ All failure simulations passed successfully!")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
