"""
Simulating Failures Test Suite

This module tests the system's ability to handle database failures, including:
- Connection errors
- Query execution errors
- Transaction rollbacks
"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, DatabaseError, ProgrammingError
from testcontainers.core.container import DockerContainer
import time

# Constants
MYSQL_VERSION = "mysql:8.0"
DATABASE_NAME = "hotel"
MYSQL_ROOT_PASSWORD = "test"

class MySQLContainer(DockerContainer):
    """Custom MySQL container implementation."""

    def __init__(self):
        super(MySQLContainer, self).__init__(MYSQL_VERSION)
        self.with_exposed_ports(3306)
        self.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        self.with_env("MYSQL_DATABASE", DATABASE_NAME)

    def get_connection_url(self):
        """Get the MySQL connection URL."""
        port = self.get_exposed_port(3306)
        return f"mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@localhost:{port}/{DATABASE_NAME}"

    def start(self):
        """Start the container and wait for MySQL to be ready."""
        super().start()
        self.wait_for_mysql_ready()
        return self

    def wait_for_mysql_ready(self, timeout=30):
        """Wait for MySQL to be ready to accept connections."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                engine = create_engine(self.get_connection_url())
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    print("✅ MySQL is ready!")
                    return
            except OperationalError:
                time.sleep(1)
        raise TimeoutError("MySQL did not become ready within the timeout period.")

@pytest.fixture(scope="module")
def mysql_container():
    """Fixture to start and stop the MySQL container."""
    container = MySQLContainer()
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="module")
def engine(mysql_container):
    """Fixture to provide a SQLAlchemy engine."""
    engine = create_engine(mysql_container.get_connection_url())
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def setup_test_db(engine):
    """Fixture to set up the test database before each test."""
    with engine.begin() as connection:
        # Drop existing table if it exists
        connection.execute(text("DROP TABLE IF EXISTS accounts"))

        # Create accounts table
        connection.execute(text("""
            CREATE TABLE accounts (
                account_id INT AUTO_INCREMENT PRIMARY KEY,
                account_name VARCHAR(50) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0)
            )
        """))

        # Insert initial data
        connection.execute(text("""
            INSERT INTO accounts (account_name, balance) VALUES
            ('Alice', 1000.00),
            ('Bob', 500.00)
        """))
        print("✅ Database setup completed successfully")
    return engine

def test_query_failure(setup_test_db):
    """Test handling of invalid SQL query."""
    with setup_test_db.connect() as connection:
        try:
            connection.execute(text("SELECT * FROM nonexistent_table"))
            pytest.fail("Expected query to fail but it succeeded")
        except ProgrammingError as e:
            print(f"✅ Query failure handled correctly: {str(e)[:100]}...")
            assert True

def test_transaction_rollback(setup_test_db):
    """Test transaction rollback on failure."""
    engine = setup_test_db
    try:
        with engine.begin() as connection:
            # Get initial balances
            result = connection.execute(text(
                "SELECT account_name, balance FROM accounts ORDER BY account_name"
            ))
            initial_balances = {row[0]: float(row[1]) for row in result}
            print(f"Initial balances: {initial_balances}")

            # Attempt to perform invalid transaction
            try:
                connection.execute(text(
                    "UPDATE accounts SET balance = balance - 2000 WHERE account_name = 'Alice'"
                ))
                pytest.fail("Expected transaction to fail due to CHECK constraint")
            except DatabaseError as e:
                print(f"✅ Expected error caught: {str(e)[:100]}...")
                # Transaction will automatically rollback

        # Verify balances in a new transaction
        with engine.begin() as connection:
            result = connection.execute(text(
                "SELECT account_name, balance FROM accounts ORDER BY account_name"
            ))
            final_balances = {row[0]: float(row[1]) for row in result}
            print(f"Final balances: {final_balances}")

            assert initial_balances == final_balances, \
                f"Balances changed after rollback\nInitial: {initial_balances}\nFinal: {final_balances}"
            print("✅ Account balances verified after rollback")

    except Exception as e:
        pytest.fail(f"Unexpected error in transaction test: {str(e)}")

@pytest.mark.simulating_failures
def test_simulating_failures(setup_test_db):
    """Test various database failure scenarios."""
    engine = setup_test_db

    # Test 1: Query Failure
    print("\nTesting query failure handling...")
    test_query_failure(engine)

    # Test 2: Transaction Rollback
    print("\nTesting transaction rollback...")
    test_transaction_rollback(engine)

    print("\n✅ All failure simulation tests completed successfully!")
