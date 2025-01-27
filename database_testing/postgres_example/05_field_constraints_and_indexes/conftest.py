"""
conftest.py - Pytest Fixtures for PostgreSQL Testcontainers

This file sets up a temporary PostgreSQL container using Testcontainers.
It provides reusable fixtures for PostgreSQL connections and cursors.
"""

import pytest
from testcontainers.postgres import PostgresContainer
import psycopg2

@pytest.fixture(scope="session")
def postgres_container():
    """
    Starts a PostgreSQL Testcontainer before running tests.

    Yields:
    - PostgreSQL container instance
    """
    container = PostgresContainer("postgres:latest")
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="session")
def postgres_connection(postgres_container):
    """
    Provides a PostgreSQL connection connected to the running Testcontainer.

    Yields:
    - psycopg2 connection instance
    """
    connection = psycopg2.connect(
        host=postgres_container.get_container_host_ip(),
        port=postgres_container.get_exposed_port(5432),
        user="test",
        password="test",
        dbname="test"
    )
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def postgres_cursor(postgres_connection):
    """
    Provides a PostgreSQL cursor for executing queries.

    Yields:
    - PostgreSQL cursor instance
    """
    cursor = postgres_connection.cursor()
    yield cursor
    cursor.close()
