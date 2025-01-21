"""
04_performance_testing.py - Demonstrates performance testing in MySQL with Testcontainers.

This example inserts and retrieves a large number of records to measure database performance.
"""

import pytest
import time

def test_insert_performance(create_table, mysql_connection):
    """Test bulk insert performance."""
    cursor = create_table
    start_time = time.time()
    for i in range(10000):
        cursor.execute("INSERT INTO performance_tests (name, value) VALUES (%s, %s)", (f"Test {i}", i))
    mysql_connection.commit()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Bulk insert time: {execution_time:.2f} seconds")
    assert execution_time < 10  # Ensure bulk insert is efficient


def test_query_performance(create_table, mysql_connection):
    """Test query performance on a large dataset."""
    cursor = create_table
    cursor.execute("SELECT COUNT(*) FROM performance_tests")
    count = cursor.fetchone()[0]
    start_time = time.time()
    cursor.execute("SELECT * FROM performance_tests WHERE value BETWEEN 5000 AND 6000")
    results = cursor.fetchall()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Query execution time: {execution_time:.2f} seconds")
    assert len(results) > 0  # Ensure query returns results
    assert execution_time < 5  # Ensure query is efficient