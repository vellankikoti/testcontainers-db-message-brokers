"""
conftest.py - Shared fixtures for MySQL resilience testing using Testcontainers.
"""

import pytest
import time
from testcontainers.mysql import MySqlContainer
import pymysql

# MySQL Configuration
MYSQL_ROOT_PASSWORD = "rootpassword"
MYSQL_USER = "testuser"
MYSQL_PASSWORD = "testpassword"
MYSQL_DATABASE = "testdb"

@pytest.fixture(scope="module")
def mysql_container():
    """Start a MySQL container using Testcontainers with proper authentication settings."""
    mysql = MySqlContainer("mysql:8.0") \
        .with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD) \
        .with_env("MYSQL_DATABASE", MYSQL_DATABASE) \
        .with_command("--default-authentication-plugin=mysql_native_password")  # ✅ Fix PyMySQL issues

    print("🚀 Starting MySQL container...")
    mysql.start()
    time.sleep(15)  # ✅ Ensure MySQL is fully initialized

    # Get MySQL host & port
    host = mysql.get_container_host_ip()
    port = int(mysql.get_exposed_port(3306))  # ✅ Ensure port is an integer

    print("🔧 Configuring MySQL users...")

    # ✅ **First connection using ROOT**
    for attempt in range(10):
        try:
            root_conn = pymysql.connect(
                host=host,
                user="root",
                password=MYSQL_ROOT_PASSWORD,
                database="mysql",
                port=port,
                cursorclass=pymysql.cursors.DictCursor,
            )
            print("✅ Connected to MySQL as root")
            break
        except pymysql.err.OperationalError as e:
            print(f"🔄 Waiting for MySQL root connection... Attempt {attempt + 1}/10: {e}")
            time.sleep(5)
    else:
        pytest.fail("❌ MySQL root connection failed!")

    # **Create User & Grant Permissions**
    cursor = root_conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};")
    cursor.execute(f"CREATE USER IF NOT EXISTS '{MYSQL_USER}'@'%' IDENTIFIED WITH mysql_native_password BY '{MYSQL_PASSWORD}';")
    cursor.execute(f"GRANT ALL PRIVILEGES ON {MYSQL_DATABASE}.* TO '{MYSQL_USER}'@'%';")
    cursor.execute("FLUSH PRIVILEGES;")
    root_conn.commit()
    cursor.close()
    root_conn.close()

    print("✅ MySQL user and permissions setup completed.")

    yield mysql  # Pass the container to the test

    print("🛑 Stopping MySQL container...")
    mysql.stop()


@pytest.fixture(scope="function")
def mysql_client(mysql_container):
    """Create a fresh MySQL connection after container restart."""
    host = mysql_container.get_container_host_ip()
    port = int(mysql_container.get_exposed_port(3306))  # ✅ Ensure port is an integer

    for attempt in range(10):  # ✅ Retry logic for connecting to MySQL
        try:
            conn = pymysql.connect(
                host=host,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                port=port,
                cursorclass=pymysql.cursors.DictCursor,
            )
            print(f"✅ MySQL connection established on {host}:{port}")
            yield conn
            conn.close()
            return
        except pymysql.err.OperationalError as e:
            print(f"🔄 Waiting for MySQL to become available (Attempt {attempt + 1}/10)... {e}")
            time.sleep(2)

    pytest.fail("❌ MySQL did not start within the expected time!")


@pytest.fixture(scope="function")
def test_table(mysql_client):
    """Set up a dedicated test table for resilience testing."""
    cursor = mysql_client.cursor()

    # Ensure table exists before running tests
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            age INT
        );
    """)

    # Cleanup before and after tests
    cursor.execute("DELETE FROM users;")
    mysql_client.commit()

    yield cursor  # Pass the cursor to tests

    # Cleanup after test execution
    cursor.execute("DELETE FROM users;")
    mysql_client.commit()
    cursor.close()
