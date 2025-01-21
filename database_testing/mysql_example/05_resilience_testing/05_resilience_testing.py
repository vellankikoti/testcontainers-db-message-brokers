"""
Extended Stays Test Suite

This module tests scenarios where guests extend their stays, including:
- Updating bookings with new check-out dates
- Recalculating total prices based on the extended stay
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from testcontainers.core.container import DockerContainer
from sqlalchemy.exc import OperationalError
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
            ('Suite', 250.00)
        """))

        # Insert booking data
        connection.execute(text("""
            INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price) VALUES
            (1, 'Alice', :today, :tomorrow, 100.00),
            (2, 'Bob', :today, :plus_two, 300.00)
        """), {
            'today': today,
            'tomorrow': today + timedelta(days=1),
            'plus_two': today + timedelta(days=2)
        })

@pytest.mark.extended_stays
def test_extended_stays():
    """Test extended stays by updating bookings and recalculating total prices."""
    mysql = MySQLContainer()
    mysql.start()

    try:
        engine = create_engine(mysql.get_connection_url())

        # Setup database and insert data
        setup_database(engine)
        insert_sample_data(engine)

        # Extend Alice's stay by 2 days
        with engine.begin() as connection:
            result = connection.execute(text("""
                SELECT rate FROM rooms WHERE room_id = 1
            """))
            rate = result.scalar()

            new_check_out = datetime.now().date() + timedelta(days=3)
            connection.execute(text("""
                UPDATE bookings
                SET check_out = :new_check_out,
                    total_price = total_price + :additional_price
                WHERE booking_id = 1
            """), {
                'new_check_out': new_check_out,
                'additional_price': rate * 2
            })

            # Verify the updated booking
            result = connection.execute(text("""
                SELECT check_out, total_price FROM bookings WHERE booking_id = 1
            """))
            row = result.fetchone()
            check_out_date = row[0]  # Access by index instead of key
            total_price = row[1]

            assert check_out_date == new_check_out, \
                f"Expected check-out date to be {new_check_out}, but got {check_out_date}"
            assert float(total_price) == 300.00, \
                f"Expected total price to be 300.00, but got {total_price}"

            print("✅ Extended stay test passed!")

    finally:
        mysql.stop()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
