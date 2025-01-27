"""
conftest.py - Shared fixtures for MySQL resilience testing using Testcontainers.
"""

import pytest
import time
from testcontainers.mysql import MySqlContainer
import pymysql

# MySQL Configuration
MYSQL_USER = "testuser"
MYSQL_PASSWORD = "testpassword"
MYSQL_DATABASE = "testdb"

@pytest.fixture(scope="module")
def mysql_container():
    """Start a MySQL container using Testcontainers."""
    mysql = MySqlContainer("mysql:8.0") \
        .with_username(MYSQL_USER) \
        .with_password(MYSQL_PASSWORD) \
        .with_database(MYSQL_DATABASE)

    print("🚀 Starting MySQL container...")
    mysql.start()
    time.sleep(5)  # Ensure MySQL initializes properly

    yield mysql

    print("🛑 Stopping MySQL container...")
    mysql.stop()


@pytest.fixture(scope="function")
def mysql_client(mysql_container):
    """Create a fresh MySQL connection after container restart."""
    for _ in range(10):
        try:
            conn = pymysql.connect(
                host=mysql_container.get_container_host_ip(),
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=mysql_container.get_exposed_port(3306),
                cursorclass=pymysql.cursors.DictCursor,
            )
            yield conn
            conn.close()
            return
        except Exception:
            print("🔄 Waiting for MySQL to become available...")
            time.sleep(2)

    pytest.fail("❌ MySQL did not start within the expected time!")

@pytest.fixture(scope="function")
def test_table(mysql_client):
    """Set up a dedicated test table for resilience testing."""
    cursor = mysql_client.cursor()
    
    # Create table if not exists
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), age INT);")

    # Cleanup before and after tests
    cursor.execute("DELETE FROM users;")
    mysql_client.commit()
    
    yield cursor
    
    cursor.execute("DELETE FROM users;")
    mysql_client.commit()
    cursor.close()
