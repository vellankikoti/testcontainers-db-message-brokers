"""
Basic Guest Management Test Suite

This module contains tests for basic CRUD (Create, Read, Update, Delete) operations
for a guest management system using PostgreSQL with testcontainers.

Tests cover:
- Guest registration (Create & Read)
- Guest information updates (Update)
- Guest removal (Delete)
"""

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text

# Constants
POSTGRES_VERSION = "postgres:15.3"
CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS guests (
        guest_id SERIAL PRIMARY KEY,
        guest_name TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

def setup_database(connection):
    """Set up the database schema."""
    connection.execute(text(CREATE_TABLE_QUERY))
    connection.commit()

@pytest.mark.basic
def test_basic_guest_insertion():
    """
    Test guest registration functionality.

    Verifies that:
    1. Multiple guests can be registered simultaneously
    2. Guest records are stored correctly
    3. All registered guests can be retrieved
    """
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        try:
            with engine.connect() as connection:
                # Initialize database
                setup_database(connection)

                # Register test guests
                test_guests = [('Alice', ), ('Bob', )]
                connection.execute(
                    text("INSERT INTO guests (guest_name) VALUES (:name)"),
                    [{"name": guest[0]} for guest in test_guests]
                )
                connection.commit()

                # Verify guest registration
                result = connection.execute(text(
                    "SELECT guest_name FROM guests ORDER BY guest_name"
                ))
                registered_guests = [row[0] for row in result]

                # Assertions
                assert len(registered_guests) == 2, "Expected exactly 2 guests"
                assert registered_guests == ['Alice', 'Bob'], "Guest list doesn't match expected names"

                print(f"✨ Successfully registered guests: {', '.join(registered_guests)}")

        except Exception as e:
            pytest.fail(f"Guest registration test failed: {str(e)}")

@pytest.mark.basic
def test_guest_deletion():
    """
    Test guest deletion functionality.

    Verifies that:
    1. A guest can be successfully deleted
    2. The deletion is permanent
    3. Only the targeted guest is removed
    """
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        try:
            with engine.connect() as connection:
                setup_database(connection)

                # Add test guests
                connection.execute(text(
                    "INSERT INTO guests (guest_name) VALUES ('Charlie'), ('David')"
                ))
                connection.commit()

                # Delete specific guest
                connection.execute(text(
                    "DELETE FROM guests WHERE guest_name = 'Charlie'"
                ))
                connection.commit()

                # Verify deletion
                result = connection.execute(text(
                    "SELECT guest_name FROM guests"
                ))
                remaining_guests = [row[0] for row in result]

                assert 'Charlie' not in remaining_guests, "Deleted guest should not be present"
                assert 'David' in remaining_guests, "Non-deleted guest should still be present"

                print("✨ Successfully verified guest deletion")

        except Exception as e:
            pytest.fail(f"Guest deletion test failed: {str(e)}")

@pytest.mark.basic
def test_guest_update():
    """
    Test guest information update functionality.

    Verifies that:
    1. Guest information can be updated
    2. Updates are persisted correctly
    3. Only the targeted guest record is modified
    """
    with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())

        try:
            with engine.connect() as connection:
                setup_database(connection)

                # Add initial guest
                connection.execute(text(
                    "INSERT INTO guests (guest_name) VALUES ('David')"
                ))
                connection.commit()

                # Update guest name
                connection.execute(text(
                    "UPDATE guests SET guest_name = 'Dave' WHERE guest_name = 'David'"
                ))
                connection.commit()

                # Verify update
                result = connection.execute(text(
                    "SELECT guest_name FROM guests WHERE guest_name = 'Dave'"
                ))
                updated_name = result.scalar()

                assert updated_name == 'Dave', "Guest name should have been updated to 'Dave'"

                # Verify no other records exist
                result = connection.execute(text("SELECT COUNT(*) FROM guests"))
                total_guests = result.scalar()
                assert total_guests == 1, "Should only have one guest record"

                print("✨ Successfully verified guest information update")

        except Exception as e:
            pytest.fail(f"Guest update test failed: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
