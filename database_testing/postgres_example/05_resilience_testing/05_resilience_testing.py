"""
Extended Stays Test Suite

This module tests the handling of extended stays in the "Happy Hotel" database, including:
- Identifying long-term bookings
- Calculating discounts for extended stays
- Verifying the accuracy of extended stay data
"""

import pytest
from datetime import datetime, timedelta
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text

# Constants
POSTGRES_VERSION = "postgres:15.3"

def setup_database(connection):
    """Initialize the database schema with rooms and bookings tables."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id SERIAL PRIMARY KEY,
            room_type TEXT NOT NULL,
            rate DECIMAL(10,2) NOT NULL,
            status TEXT DEFAULT 'available'
        );

        CREATE TABLE IF NOT EXISTS bookings (
            booking_id SERIAL PRIMARY KEY,
            room_id INT NOT NULL,
            guest_name TEXT NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id),
            CONSTRAINT valid_dates CHECK (check_out > check_in)
        );
    """))
    connection.commit()

def insert_sample_data(connection):
    """Insert sample rooms and bookings data."""
    # Insert room data
    connection.execute(text("""
        INSERT INTO rooms (room_type, rate) VALUES
        ('Standard', 100.00),
        ('Deluxe', 150.00),
        ('Suite', 250.00);
    """))

    # Insert booking data
    today = datetime.now().date()
    connection.execute(text("""
        INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price) VALUES
        (1, 'Alice', :today, :plus_seven, 700.00),
        (2, 'Bob', :today, :plus_fourteen, 2000.00),
        (3, 'Charlie', :today, :plus_three, 300.00);
    """), {
        'today': today,
        'plus_seven': today + timedelta(days=7),
        'plus_fourteen': today + timedelta(days=14),
        'plus_three': today + timedelta(days=3)
    })
    connection.commit()

def calculate_extended_stays(connection, min_days=7):
    """Identify extended stays and calculate discounts."""
    return connection.execute(text("""
        SELECT 
            b.booking_id,
            b.guest_name,
            b.check_in,
            b.check_out,
            b.total_price,
            (b.check_out - b.check_in) AS stay_length,
            CASE 
                WHEN (b.check_out - b.check_in) >= :min_days THEN ROUND(b.total_price * 0.9, 2)
                ELSE b.total_price
            END AS discounted_price
        FROM bookings b
        WHERE (b.check_out - b.check_in) >= :min_days
        ORDER BY b.booking_id;
    """), {'min_days': min_days}).fetchall()

@pytest.mark.extended_stays
def test_extended_stays():
    """Test the identification and discount calculation for extended stays."""
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as connection:
            # Setup and insert sample data
            setup_database(connection)
            insert_sample_data(connection)

            # Calculate extended stays
            extended_stays = calculate_extended_stays(connection, min_days=7)

            # Verify results
            assert len(extended_stays) == 2, "There should be 2 extended stays."
            for stay in extended_stays:
                stay_length = stay.stay_length  # Now directly using the integer
                assert stay_length >= 7, f"Stay length should be at least 7 days, got {stay_length}."
                assert stay.discounted_price < stay.total_price, "Discounted price should be less than total price."

            # Print extended stays
            print("\n📊 Extended Stays Report:")
            for stay in extended_stays:
                print(f"Booking ID: {stay.booking_id}, Guest: {stay.guest_name}, "
                      f"Stay Length: {stay.stay_length} days, "
                      f"Original Price: ${stay.total_price}, Discounted Price: ${stay.discounted_price}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
