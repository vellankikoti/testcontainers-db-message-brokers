"""
Occupancy Report Test Suite

This module tests the generation of hotel occupancy reports, including:
- Daily occupancy rates
- Room type availability
- Revenue calculations
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
        ('Suite', 250.00),
        ('Standard', 100.00),
        ('Deluxe', 150.00);
    """))

    # Insert booking data
    today = datetime.now().date()
    connection.execute(text("""
        INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price) VALUES
        (1, 'Alice', :today, :tomorrow, 100.00),
        (2, 'Bob', :today, :plus_two, 300.00),
        (3, 'Charlie', :tomorrow, :plus_three, 500.00);
    """), {
        'today': today,
        'tomorrow': today + timedelta(days=1),
        'plus_two': today + timedelta(days=2),
        'plus_three': today + timedelta(days=3)
    })
    connection.commit()

def calculate_occupancy_rate(connection, date):
    """Calculate the occupancy rate for a specific date."""
    result = connection.execute(text("""
        SELECT 
            COUNT(DISTINCT b.room_id)::float / COUNT(DISTINCT r.room_id)::float * 100 as occupancy_rate
        FROM rooms r
        LEFT JOIN bookings b ON r.room_id = b.room_id
        AND :date BETWEEN b.check_in AND b.check_out - 1
    """), {'date': date}).fetchone()
    
    return result[0] if result[0] is not None else 0.0

def generate_occupancy_report(connection, start_date):
    """Generate a detailed occupancy report."""
    return connection.execute(text("""
        WITH daily_occupancy AS (
            SELECT 
                d.date,
                COUNT(DISTINCT b.room_id) as occupied_rooms,
                COUNT(DISTINCT r.room_id) as total_rooms,
                SUM(CASE 
                    WHEN b.room_id IS NOT NULL 
                    THEN r.rate 
                    ELSE 0 
                END) as daily_revenue
            FROM generate_series(:start_date, 
                               :start_date + INTERVAL '6 days', 
                               INTERVAL '1 day') as d(date)
            CROSS JOIN rooms r
            LEFT JOIN bookings b ON r.room_id = b.room_id
            AND d.date BETWEEN b.check_in AND b.check_out - 1
            GROUP BY d.date
        )
        SELECT 
            date,
            occupied_rooms,
            total_rooms,
            ROUND((occupied_rooms::float / total_rooms::float * 100)::numeric, 2) as occupancy_rate,
            daily_revenue
        FROM daily_occupancy
        ORDER BY date;
    """), {'start_date': start_date}).fetchall()

@pytest.mark.occupancy
def test_occupancy_calculation():
    """Test the calculation of hotel occupancy rates."""
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())
        
        with engine.connect() as connection:
            # Setup and insert sample data
            setup_database(connection)
            insert_sample_data(connection)
            
            # Calculate occupancy for today
            today = datetime.now().date()
            occupancy_rate = calculate_occupancy_rate(connection, today)
            
            # Verify occupancy rate
            assert 0 <= occupancy_rate <= 100, "Occupancy rate should be between 0 and 100"
            assert occupancy_rate == 40.0, f"Expected 40% occupancy, got {occupancy_rate}%"

@pytest.mark.occupancy
def test_weekly_report():
    """Test the generation of a weekly occupancy report."""
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())
        
        with engine.connect() as connection:
            # Setup and insert sample data
            setup_database(connection)
            insert_sample_data(connection)
            
            # Generate weekly report
            today = datetime.now().date()
            report = generate_occupancy_report(connection, today)
            
            # Verify report data
            assert len(report) == 7, "Weekly report should cover 7 days"
            
            # Print report
            print("\n📊 Weekly Occupancy Report:")
            for day in report:
                print(f"Date: {day[0]}, Occupancy: {day[3]}%, Revenue: ${day[4]}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
