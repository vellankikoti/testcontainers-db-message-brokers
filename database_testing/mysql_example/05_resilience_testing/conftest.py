"""
conftest.py - Shared fixtures for MySQL resilience testing using Docker API.
"""

import pytest
import time
import docker
import pymysql

MYSQL_USER = "testuser"
MYSQL_PASSWORD = "testpassword"
MYSQL_DATABASE = "testdb"
MYSQL_PORT = 3306


@pytest.fixture(scope="module")
def mysql_container():
    """Start a MySQL container with a fixed name to persist across restarts using Docker API."""
    client = docker.from_env()

    try:
        container = client.containers.get("mysql-testcontainer")
        print("♻️ Reusing existing MySQL container...")
        container.start()
    except docker.errors.NotFound:
        container = client.containers.run(
            "mysql:8.0",
            name="mysql-testcontainer",
            environment={
                "MYSQL_ROOT_PASSWORD": MYSQL_PASSWORD,
                "MYSQL_USER": MYSQL_USER,
                "MYSQL_PASSWORD": MYSQL_PASSWORD,
                "MYSQL_DATABASE": MYSQL_DATABASE,
            },
            ports={"3306/tcp": MYSQL_PORT},
            detach=True,
            remove=False,  # Don't auto-remove container
        )
        print("🚀 Starting a new MySQL container...")

    time.sleep(10)  # Ensure MySQL initializes properly

    yield container

    print("🛑 Stopping MySQL container...")
    container.stop()


@pytest.fixture(scope="function")
def mysql_client():
    """Create a fresh MySQL connection after container restart."""
    for _ in range(10):
        try:
            conn = pymysql.connect(
                host="localhost",
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=MYSQL_PORT,
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
