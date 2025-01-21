"""
conftest.py - Shared fixtures for MySQL example
"""

import pytest
from testcontainers.mysql import MySqlContainer
import mysql.connector

@pytest.fixture(scope="module")
def mysql_container():
    """Start a MySQL container and provide the connection details."""
    with MySqlContainer("mysql:8.0") as mysql:
        yield mysql

@pytest.fixture(scope="module")
def mysql_connection(mysql_container):
    """Create a MySQL connection using the container credentials."""
    connection = mysql.connector.connect(
        host=mysql_container.get_container_host_ip(),
        port=mysql_container.get_exposed_port(3306),
        user=mysql_container.USER,
        password=mysql_container.PASSWORD,
        database=mysql_container.DBNAME
    )
    yield connection
    connection.close()

@pytest.fixture(scope="module")
def create_table(mysql_connection):
    """Set up a test table for schema validation."""
    cursor = mysql_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            age INT CHECK (age > 0)
        )
    """)
    mysql_connection.commit()
    yield cursor
    cursor.execute("DROP TABLE users")
    mysql_connection.commit()
    cursor.close()