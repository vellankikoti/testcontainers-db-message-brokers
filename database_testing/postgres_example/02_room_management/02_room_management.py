"""
Room Management Test Suite

This module contains tests for hotel room management functionality, including:
- Room inventory management
- Room pricing operations
- Room availability tracking
"""

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from decimal import Decimal

# Constants
POSTGRES_VERSION = "postgres:15.3"
CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS rooms (
        room_id SERIAL PRIMARY KEY,
        room_type TEXT NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        is_available BOOLEAN DEFAULT true
    );
"""

# Test Data
SAMPLE_ROOMS = [
    ("Single", 100.00),
    ("Double", 150.00),
    ("Suite", 300.00)
]

def setup_database(connection):
    """Initialize the database schema."""
    connection.execute(text(CREATE_TABLE_QUERY))
    connection.commit()

def insert_sample_rooms(connection):
    """Insert sample room data for testing."""
    connection.execute(text("""
        INSERT INTO rooms (room_type, price)
        VALUES (:type, :price)
    """), [{"type": room[0], "price": room[1]} for room in SAMPLE_ROOMS])
    connection.commit()

@pytest.mark.rooms
def test_room_management():
    """
    Test room inventory and pricing management.

    Verifies:
    1. Room data is stored correctly.
    2. Room availability can be updated.
    3. Room pricing is accurate.
    """
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        try:
            with engine.connect() as connection:
                # Setup database and insert sample data
                setup_database(connection)
                insert_sample_rooms(connection)

                # Verify room count
                result = connection.execute(text("SELECT COUNT(*) FROM rooms"))
                count = result.scalar()
                assert count == len(SAMPLE_ROOMS), f"Expected {len(SAMPLE_ROOMS)} rooms, got {count}"

                # Verify room data
                result = connection.execute(text("SELECT room_type, price FROM rooms ORDER BY price"))
                rooms = {row[0]: Decimal(str(row[1])) for row in result}
                assert rooms["Single"] == Decimal("100.00"), "Single room price mismatch"
                assert rooms["Double"] == Decimal("150.00"), "Double room price mismatch"
                assert rooms["Suite"] == Decimal("300.00"), "Suite room price mismatch"

                # Update room availability
                connection.execute(text("""
                    UPDATE rooms
                    SET is_available = false
                    WHERE room_type = 'Single'
                """))
                connection.commit()

                # Verify availability update
                result = connection.execute(text("""
                    SELECT is_available FROM rooms WHERE room_type = 'Single'
                """))
                is_available = result.scalar()
                assert not is_available, "Single room should be marked as unavailable"

                print("🏠 Room management test passed successfully!")

        except Exception as e:
            pytest.fail(f"Test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
