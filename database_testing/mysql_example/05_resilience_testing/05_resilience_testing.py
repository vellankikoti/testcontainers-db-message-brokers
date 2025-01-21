"""
05_resilience_testing.py - Demonstrates resilience testing in MySQL with Testcontainers.

This example simulates MySQL failures and verifies recovery mechanisms.
"""

import pytest
import time
from mysql.connector.errors import OperationalError

def test_reconnect_after_failure(create_table, mysql_container):
    """Test that MySQL can recover after being stopped and restarted."""
    cursor = create_table
    cursor.execute("INSERT INTO resilience_tests (name, value) VALUES (%s, %s)", ("Before Failure", 100))
    mysql_container.stop()
    time.sleep(5)  # Simulate downtime
    mysql_container.start()
    time.sleep(5)  # Allow MySQL to restart
    connection = mysql_container.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM resilience_tests")
    count = cursor.fetchone()[0]
    assert count == 1  # Ensure data persistence after restart


def test_query_timeout_handling(create_table, mysql_connection):
    """Test how MySQL handles query timeouts."""
    cursor = create_table
    try:
        cursor.execute("SELECT SLEEP(5)")  # Simulating long-running query
    except OperationalError:
        assert True  # Expected behavior on timeout
    else:
        assert False  # Query should time out in production scenarios