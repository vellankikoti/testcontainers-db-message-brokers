"""
conftest.py - Pytest Fixtures for MySQL Testcontainers

This file sets up a temporary MySQL container using Testcontainers.
It provides reusable fixtures for MySQL connections and cursors.
"""

import pytest
from testcontainers.mysql import MySqlContainer
import mysql.connector

@pytest.fixture(scope="session")
def mysql_container():
    """
    Starts a MySQL Testcontainer before running tests.

    Yields:
    - MySQL container instance
    """
    container = MySqlContainer("mysql:latest")
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="session")
def mysql_connection(mysql_container):
    """
    Provides a MySQL connection connected to the running Testcontainer.

    Yields:
    - mysql.connector.connect instance
    """
    connection = mysql.connector.connect(
        host=mysql_container.get_container_host_ip(),
        port=mysql_container.get_exposed_port(3306),
        user="test",
        password="test",
        database="test"
    )
    yield connection
    connection.close()

@pytest.fixture(scope="function")
def mysql_cursor(mysql_connection):
    """
    Provides a MySQL cursor for executing queries.

    Yields:
    - MySQL cursor instance
    """
    cursor = mysql_connection.cursor()
    yield cursor
    cursor.close()
