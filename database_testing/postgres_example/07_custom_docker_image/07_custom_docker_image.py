"""
Custom Docker Image Test Suite

This module demonstrates how to use a custom Docker image for testing,
including verification of preloaded data and custom configurations.
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from sqlalchemy import create_engine, text


class CustomPostgresContainer(DockerContainer):
    """Custom PostgreSQL container class."""

    def __init__(self):
        super().__init__("custom-postgres:1.0")
        self.with_exposed_ports(5432)
        self.with_env("POSTGRES_DB", "testdb")
        self.with_env("POSTGRES_USER", "testuser")
        self.with_env("POSTGRES_PASSWORD", "testpass")

    def get_connection_url(self):
        """Get the database connection URL."""
        port = self.get_exposed_port(5432)
        return f"postgresql://testuser:testpass@localhost:{port}/testdb"

    def wait_for_database(self):
        """Wait for the database to be ready."""
        max_retries = 10
        retry_interval = 2  # seconds

        for attempt in range(max_retries):
            try:
                engine = create_engine(self.get_connection_url())
                with engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                print("✅ Database is ready!")
                return
            except Exception as e:
                print(f"Waiting for database... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_interval)

        raise RuntimeError("Database did not become ready in time.")


def verify_preloaded_data(connection):
    """Verify that the preloaded data exists and is correct."""
    try:
        # Check if tables exist
        tables = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)).fetchall()
        
        print(f"Found tables: {[table[0] for table in tables]}")

        # Check hotels
        hotels = connection.execute(text("""
            SELECT name, location, rating 
            FROM hotels 
            ORDER BY hotel_id;
        """)).fetchall()

        assert len(hotels) == 3, f"Expected 3 hotels in preloaded data, got {len(hotels)}"
        assert hotels[0][0] == "Grand Hotel", f"First hotel should be Grand Hotel, got {hotels[0][0]}"

        # Check amenities
        amenities = connection.execute(text("""
            SELECT h.name as hotel, a.name as amenity
            FROM amenities a
            JOIN hotels h ON h.hotel_id = a.hotel_id
            ORDER BY h.hotel_id, a.amenity_id;
        """)).fetchall()

        assert len(amenities) == 4, f"Expected 4 amenities in preloaded data, got {len(amenities)}"
        
        print("✅ Preloaded data verification successful!")
        
    except Exception as e:
        print(f"❌ Error during data verification: {str(e)}")
        raise


@pytest.mark.custom_docker
def test_custom_docker_image():
    """Test the custom Docker image with preloaded data."""
    print("\nStarting custom Docker image test...")
    
    with CustomPostgresContainer() as postgres:
        print("\nContainer started, waiting for database...")
        
        # Wait for the database to be ready
        postgres.wait_for_database()

        print("\nCreating database connection...")
        engine = create_engine(postgres.get_connection_url())

        with engine.connect() as connection:
            print("\nVerifying preloaded data...")
            verify_preloaded_data(connection)

            print("\nTesting data insertion...")
            # Test inserting new data
            connection.execute(text("""
                INSERT INTO hotels (name, location, rating)
                VALUES ('City Center Hotel', 'Chicago', 4);
            """))
            connection.commit()

            # Verify the new data
            result = connection.execute(text("""
                SELECT COUNT(*) FROM hotels;
            """)).scalar()

            assert result == 4, f"Expected 4 hotels after insertion, got {result}"

            print("\n✅ Custom Docker image loaded successfully!")
            print("✅ Data insertion test passed!")
            print("✅ All tests completed successfully!")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
