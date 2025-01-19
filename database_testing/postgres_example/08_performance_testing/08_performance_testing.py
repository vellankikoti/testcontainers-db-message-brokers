"""
Performance Testing Suite

This module tests the performance of database queries and operations, including:
- Measuring query execution time.
- Testing performance under load.
- Identifying potential bottlenecks.
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from sqlalchemy import create_engine, text


class PerformancePostgresContainer(DockerContainer):
    """Custom PostgreSQL container for performance testing."""

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


def measure_query_time(connection, query):
    """Measure the execution time of a query."""
    start_time = time.time()
    connection.execute(text(query))
    end_time = time.time()
    return end_time - start_time


@pytest.mark.performance
def test_query_performance():
    """Test the performance of database queries."""
    with PerformancePostgresContainer() as postgres:
        postgres.wait_for_database()

        engine = create_engine(postgres.get_connection_url())
        with engine.connect() as connection:
            # Measure the time to fetch all rows from a large table
            query = "SELECT * FROM bookings;"
            execution_time = measure_query_time(connection, query)

            print(f"Query execution time: {execution_time:.2f} seconds")
            assert execution_time < 1.0, "Query took too long to execute!"

            # Test inserting a large number of rows
            print("Testing bulk insert performance...")
            start_time = time.time()
            for i in range(1000):
                connection.execute(text("""
                    INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price)
                    VALUES (1, 'Test Guest', '2024-01-01', '2024-01-02', 100.00);
                """))
            connection.commit()
            end_time = time.time()

            bulk_insert_time = end_time - start_time
            print(f"Bulk insert execution time: {bulk_insert_time:.2f} seconds")
            assert bulk_insert_time < 5.0, "Bulk insert took too long!"

            print("✅ Performance tests passed successfully!")
