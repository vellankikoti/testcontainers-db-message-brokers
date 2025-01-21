"""
Reservations Test Suite

This module tests the management of hotel reservations, including:
- Creating a `reservations` table
- Inserting reservation data
- Validating reservation constraints
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

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

def setup_database(connection):
    """Initialize the database schema with a reservations table."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id INT AUTO_INCREMENT PRIMARY KEY,
            guest_name VARCHAR(100) NOT NULL,
            room_id INT NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            CONSTRAINT valid_dates CHECK (check_out > check_in)
        );
    """))
    connection.commit()

def insert_sample_data(connection):
    """Insert sample reservation data."""
    connection.execute(text("""
        INSERT INTO reservations (guest_name, room_id, check_in, check_out, total_price) VALUES
        ('Alice', 1, '2024-12-01', '2024-12-05', 400.00),
        ('Bob', 2, '2024-12-03', '2024-12-06', 450.00),
        ('Charlie', 3, '2024-12-02', '2024-12-04', 300.00);
    """))
    connection.commit()

@pytest.mark.reservations
def test_reservation_operations():
    """Test reservation operations using testcontainers."""
    # Start MySQL container
    mysql = MySQLContainer()
    mysql.start()

    try:
        # Create database connection
        engine = create_engine(mysql.get_connection_url())

        with engine.connect() as connection:
            # Setup database
            setup_database(connection)

            # Test INSERT operation
            insert_sample_data(connection)

            # Test SELECT operation: Count reservations
            result = connection.execute(text("SELECT COUNT(*) FROM reservations"))
            reservation_count = result.scalar()
            assert reservation_count == 3, f"Expected 3 reservations, but found {reservation_count}"

            # Test SELECT operation: Validate total price
            result = connection.execute(text("""
                SELECT total_price FROM reservations WHERE guest_name = 'Alice'
            """))
            total_price = result.scalar()
            assert total_price == 400.00, f"Expected total price 400.00, but found {total_price}"

            # Test UPDATE operation: Update total price
            connection.execute(text("""
                UPDATE reservations SET total_price = 500.00 WHERE guest_name = 'Alice'
            """))
            connection.commit()

            # Verify UPDATE
            result = connection.execute(text("""
                SELECT total_price FROM reservations WHERE guest_name = 'Alice'
            """))
            updated_price = result.scalar()
            assert updated_price == 500.00, f"Expected updated price 500.00, but found {updated_price}"

            # Test DELETE operation: Remove a reservation
            connection.execute(text("""
                DELETE FROM reservations WHERE guest_name = 'Charlie'
            """))
            connection.commit()

            # Verify DELETE
            result = connection.execute(text("SELECT COUNT(*) FROM reservations"))
            reservation_count = result.scalar()
            assert reservation_count == 2, f"Expected 2 reservations after deletion, but found {reservation_count}"

            print("✅ All reservation operations passed!")

    finally:
        mysql.stop()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
