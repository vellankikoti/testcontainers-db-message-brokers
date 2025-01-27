"""
05_resilience_testing.py - Demonstrates resilience testing in MySQL with Testcontainers.

This example simulates MySQL failures, verifies automatic recovery, and ensures data integrity.
"""

import pytest
import time
from pymysql import connect
from pymysql.err import OperationalError

@pytest.mark.resilience
def test_mysql_reconnect(mysql_container, test_table):
    """Test MySQL automatic reconnection after failure."""

    # Insert initial test data
    test_table.execute("INSERT INTO users (name, age) VALUES ('Alice', 30);")
    test_table.connection.commit()
    print("✅ Inserted initial data before failure.")

    # Ensure data is present before failure
    test_table.execute("SELECT * FROM users WHERE name = 'Alice';")
    result = test_table.fetchone()
    assert result is not None, "❌ Data not found before failure."

    # Simulate failure by stopping the container
    print("🛑 Stopping MySQL container...")
    mysql_container.stop()
    time.sleep(5)

    # Restart MySQL container
    print("🚀 Restarting MySQL container...")
    mysql_container.start()
    time.sleep(5)

    # Ensure MySQL is fully ready after restart
    print("🔄 Reconnecting to MySQL...")
    for attempt in range(10):
        try:
            new_conn = connect(
                host=mysql_container.get_container_host_ip(),
                user="testuser",
                password="testpassword",
                database="testdb",
                port=mysql_container.get_exposed_port(3306),
                cursorclass=pymysql.cursors.DictCursor,
            )
            print(f"✅ MySQL reconnected successfully after {attempt + 1} seconds")
            break
        except OperationalError:
            print(f"🔄 Retrying connection... Attempt {attempt + 1}")
            time.sleep(1)
    else:
        pytest.fail("❌ MySQL did not restart successfully!")

    # Validate data integrity
    new_cursor = new_conn.cursor()
    new_cursor.execute("SELECT * FROM users WHERE name = 'Alice';")
    retrieved_data = new_cursor.fetchone()
    assert retrieved_data is not None, "❌ Data was lost after restart!"
    print("✅ Data is still available after restart.")

    # Insert new record post-recovery
    new_cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 35);")
    new_conn.commit()

    # Validate both records exist
    new_cursor.execute("SELECT COUNT(*) AS count FROM users;")
    count = new_cursor.fetchone()["count"]
    assert count == 2, f"❌ Expected 2 records, found {count} after recovery!"
    print("✅ Successfully inserted data after recovery, test passed! 🎉")
