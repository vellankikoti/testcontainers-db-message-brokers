"""
conftest.py - Shared fixtures for PostgreSQL example
"""

import pytest
from testcontainers.postgres import PostgresContainer
import psycopg2

@pytest.fixture(scope="module")
def postgres_container():
    """Start a PostgreSQL container and provide the connection details."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture(scope="module")
def postgres_connection(postgres_container):
    """Create a PostgreSQL connection using the container credentials."""
    connection = psycopg2.connect(
        host=postgres_container.get_container_host_ip(),
        port=postgres_container.get_exposed_port(5432),
        user=postgres_container.USER,
        password=postgres_container.PASSWORD,
        dbname=postgres_container.DBNAME
    )
    yield connection
    connection.close()

@pytest.fixture(scope="module")
def create_performance_table(postgres_connection):
    """Set up a test table for performance testing."""
    cursor = postgres_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_tests (
            id SERIAL PRIMARY KEY,
            operation VARCHAR(50) NOT NULL,
            duration_ms INT NOT NULL
        )
    """)
    postgres_connection.commit()
    yield cursor
    cursor.execute("DROP TABLE performance_tests")
    postgres_connection.commit()
    cursor.close()