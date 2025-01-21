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
def create_schema(postgres_connection):
    """Set up a schema validation example."""
    cursor = postgres_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            age INT CHECK (age >= 18)
        )
    """)
    postgres_connection.commit()
    yield cursor
    cursor.execute("DROP TABLE users")
    postgres_connection.commit()
    cursor.close()