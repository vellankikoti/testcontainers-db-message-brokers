"""
Reservation System Test Suite

This module contains tests for the hotel reservation system, including:
- Reservation creation
- Reservation retrieval
- Date handling
- Data verification
"""

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text

# Constants
POSTGRES_VERSION = "postgres:15.3"
CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id SERIAL PRIMARY KEY,
        guest_name TEXT NOT NULL,
        room_type TEXT NOT NULL,
        check_in DATE NOT NULL,
        check_out DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT valid_dates CHECK (check_out > check_in)
    );
"""

# Test Data
SAMPLE_RESERVATIONS = [
    {
        "guest_name": "Alice",
        "room_type": "Single",
        "check_in": "2024-12-24",
        "check_out": "2024-12-26"
    },
    {
        "guest_name": "Bob",
        "room_type": "Suite",
        "check_in": "2024-12-25",
        "check_out": "2024-12-30"
    }
]

def setup_database(connection):
    """Initialize the database schema."""
    connection.execute(text(CREATE_TABLE_QUERY))
    connection.commit()

def insert_sample_reservations(connection):
    """Insert sample reservation data for testing."""
    insert_query = """
        INSERT INTO reservations (guest_name, room_type, check_in, check_out)
        VALUES (:guest_name, :room_type, :check_in, :check_out)
    """
    connection.execute(text(insert_query), SAMPLE_RESERVATIONS)
    connection.commit()

def get_reservations(connection):
    """Retrieve all reservations ordered by check-in date."""
    query = """
        SELECT guest_name, room_type, check_in, check_out 
        FROM reservations 
        ORDER BY check_in
    """
    result = connection.execute(text(query))
    return [
        {
            "guest_name": row[0],
            "room_type": row[1],
            "check_in": row[2],
            "check_out": row[3]
        }
        for row in result
    ]

@pytest.mark.reservations
def test_reservation_system():
    """Test reservation creation and retrieval functionality."""
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        try:
            with engine.connect() as connection:
                # Setup database and insert sample data
                setup_database(connection)
                insert_sample_reservations(connection)

                # Retrieve and verify reservations
                reservations = get_reservations(connection)

                # Verify reservation count
                assert len(reservations) == len(SAMPLE_RESERVATIONS), \
                    f"Expected {len(SAMPLE_RESERVATIONS)} reservations, got {len(reservations)}"

                # Verify reservation details
                for actual, expected in zip(reservations, SAMPLE_RESERVATIONS):
                    assert actual["guest_name"] == expected["guest_name"]
                    assert actual["room_type"] == expected["room_type"]
                    assert str(actual["check_in"]) == expected["check_in"]
                    assert str(actual["check_out"]) == expected["check_out"]

                # Print success message
                print("\n📅 Reservations created and verified successfully!")
                for res in reservations:
                    print(
                        f"Guest: {res['guest_name']:<10} "
                        f"Room: {res['room_type']:<10} "
                        f"Check-in: {res['check_in']} "
                        f"Check-out: {res['check_out']}"
                    )

        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.reservations
def test_invalid_dates():
    """Test handling of invalid reservation dates."""
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as connection:
            setup_database(connection)

            # Test check-out before check-in
            with pytest.raises(Exception):
                connection.execute(text("""
                    INSERT INTO reservations (guest_name, room_type, check_in, check_out)
                    VALUES ('Charlie', 'Double', '2024-12-26', '2024-12-24')
                """))
                connection.commit()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
