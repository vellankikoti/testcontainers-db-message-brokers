"""
04_performance_testing.py - Demonstrates performance testing in PostgreSQL with Testcontainers.

This example measures query execution times for bulk inserts and complex queries.
"""

import pytest
import time

def test_bulk_insert_performance(create_performance_table, postgres_connection):
    """Test the performance of bulk inserts."""
    cursor = create_performance_table
    start_time = time.time()
    for i in range(1000):
        cursor.execute("INSERT INTO performance_tests (operation, duration_ms) VALUES (%s, %s)",
                       ("INSERT", i))
    postgres_connection.commit()
    duration = (time.time() - start_time) * 1000  # Convert to milliseconds
    assert duration < 5000  # Expect bulk inserts to be completed within 5 seconds

def test_complex_query_performance(create_performance_table, postgres_connection):
    """Test the performance of a complex query."""
    cursor = create_performance_table
    start_time = time.time()
    cursor.execute("SELECT operation, COUNT(*) FROM performance_tests GROUP BY operation")
    results = cursor.fetchall()
    duration = (time.time() - start_time) * 1000  # Convert to milliseconds
    assert duration < 2000  # Expect query to execute within 2 seconds