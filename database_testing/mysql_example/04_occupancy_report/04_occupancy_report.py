"""
Occupancy Report Test Suite

This module tests the generation of hotel occupancy reports, including:
- Daily occupancy rates
- Room type availability
- Revenue calculations
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from datetime import datetime, timedelta

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

def setup_database(engine):
    """Initialize the database schema with rooms and bookings tables."""
    with engine.begin() as connection:
        # Drop existing tables if they exist
        connection.execute(text("DROP TABLE IF EXISTS bookings"))
        connection.execute(text("DROP TABLE IF EXISTS rooms"))

        # Create tables
        connection.execute(text("""
            CREATE TABLE rooms (
                room_id INT AUTO_INCREMENT PRIMARY KEY,
                room_type VARCHAR(50) NOT NULL,
                rate DECIMAL(10, 2) NOT NULL,
                status VARCHAR(20) DEFAULT 'available'
            )
        """))

        connection.execute(text("""
            CREATE TABLE bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                room_id INT NOT NULL,
                guest_name VARCHAR(100) NOT NULL,
                check_in DATE NOT NULL,
                check_out DATE NOT NULL,
                total_price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(room_id),
                CONSTRAINT valid_dates CHECK (check_out > check_in)
            )
        """))

def insert_sample_data(engine):
    """Insert sample rooms and bookings data."""
    today = datetime.now().date()

    with engine.begin() as connection:
        # Insert room data
        connection.execute(text("""
            INSERT INTO rooms (room_type, rate) VALUES
            ('Standard', 100.00),
            ('Deluxe', 150.00),
            ('Suite', 250.00),
            ('Standard', 100.00),
            ('Deluxe', 150.00)
        """))

        # Insert booking data
        connection.execute(text("""
            INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price) VALUES
            (1, 'Alice', :today, :tomorrow, 100.00),
            (2, 'Bob', :today, :plus_two, 300.00),
            (3, 'Charlie', :tomorrow, :plus_three, 500.00)
        """), {
            'today': today,
            'tomorrow': today + timedelta(days=1),
            'plus_two': today + timedelta(days=2),
            'plus_three': today + timedelta(days=3)
        })

@pytest.mark.occupancy_report
def test_occupancy_report():
    """Test occupancy report generation using testcontainers."""
    mysql = MySQLContainer()
    mysql.start()

    try:
        engine = create_engine(mysql.get_connection_url())

        # Setup database and insert data
        setup_database(engine)
        insert_sample_data(engine)

        # Run tests in a new transaction
        with engine.begin() as connection:
            # Test daily occupancy rate
            result = connection.execute(text("""
                SELECT COUNT(*) AS occupied_rooms
                FROM bookings
                WHERE :today BETWEEN check_in AND check_out
            """), {'today': datetime.now().date()})
            occupied_rooms = result.scalar()
            assert occupied_rooms == 2, f"Expected 2 occupied rooms, but found {occupied_rooms}"

            # Test room type availability
            result = connection.execute(text("""
                SELECT room_type, COUNT(*) AS available_rooms
                FROM rooms
                WHERE status = 'available'
                GROUP BY room_type
            """))
            available_rooms = {row[0]: row[1] for row in result}
            assert available_rooms['Standard'] == 2, f"Expected 2 available Standard rooms, but found {available_rooms['Standard']}"
            assert available_rooms['Deluxe'] == 2, f"Expected 2 available Deluxe rooms, but found {available_rooms['Deluxe']}"

            # Test revenue calculation
            result = connection.execute(text("""
                SELECT SUM(total_price) AS total_revenue
                FROM bookings
            """))
            total_revenue = result.scalar()
            assert total_revenue == 900.00, f"Expected total revenue 900.00, but found {total_revenue}"

            print("✅ All occupancy report tests passed!")

    finally:
        mysql.stop()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
