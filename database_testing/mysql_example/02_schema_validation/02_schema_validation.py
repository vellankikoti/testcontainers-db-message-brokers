"""
Room Management Test Suite

This module tests the management of hotel rooms, including:
- Creating a `rooms` table
- Inserting room data
- Updating room rates
- Checking room availability
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
    """Initialize the database schema with a rooms table."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INT AUTO_INCREMENT PRIMARY KEY,
            room_type VARCHAR(50) NOT NULL,
            rate DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) DEFAULT 'available'
        );
    """))
    connection.commit()

def insert_sample_data(connection):
    """Insert sample room data."""
    connection.execute(text("""
        INSERT INTO rooms (room_type, rate, status) VALUES
        ('Standard', 100.00, 'available'),
        ('Deluxe', 150.00, 'available'),
        ('Suite', 250.00, 'occupied'),
        ('Standard', 100.00, 'occupied'),
        ('Deluxe', 150.00, 'available');
    """))
    connection.commit()

@pytest.mark.room_management
def test_room_management_operations():
    """Test room management operations using testcontainers."""
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

            # Test SELECT operation: Count available rooms
            result = connection.execute(text("""
                SELECT COUNT(*) FROM rooms WHERE status = 'available'
            """))
            available_rooms = result.scalar()
            assert available_rooms == 3, f"Expected 3 available rooms, but found {available_rooms}"

            # Test UPDATE operation: Update room rates
            connection.execute(text("""
                UPDATE rooms SET rate = rate + 20.00 WHERE room_type = 'Standard'
            """))
            connection.commit()

            # Verify UPDATE
            result = connection.execute(text("""
                SELECT rate FROM rooms WHERE room_type = 'Standard' LIMIT 1
            """))
            updated_rate = result.scalar()
            assert updated_rate == 120.00, f"Expected updated rate 120.00, but found {updated_rate}"

            # Test DELETE operation: Remove occupied rooms
            connection.execute(text("""
                DELETE FROM rooms WHERE status = 'occupied'
            """))
            connection.commit()

            # Verify DELETE
            result = connection.execute(text("""
                SELECT COUNT(*) FROM rooms WHERE status = 'occupied'
            """))
            occupied_rooms = result.scalar()
            assert occupied_rooms == 0, f"Expected 0 occupied rooms, but found {occupied_rooms}"

            print("✅ All room management operations passed!")

    finally:
        mysql.stop()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
