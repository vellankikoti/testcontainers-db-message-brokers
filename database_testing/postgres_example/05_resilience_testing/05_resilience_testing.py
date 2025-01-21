"""
05_resilience_testing.py - Demonstrates resilience testing in PostgreSQL with Testcontainers.

This example tests database reconnections, transaction integrity, and recovery from failures.
"""

import pytest
import time

def test_database_reconnection(create_resilience_table, postgres_connection):
    """Test database reconnection after temporary failure."""
    cursor = create_resilience_table
    cursor.execute("INSERT INTO resilience_tests (test_case, result) VALUES (%s, %s) RETURNING id",
                   ("Initial Insert", "SUCCESS"))
    postgres_connection.commit()
    
    postgres_connection.close()  # Simulate database failure
    time.sleep(3)  # Wait before reconnecting
    
    new_connection = postgres_connection.cursor()
    new_connection.execute("SELECT result FROM resilience_tests WHERE test_case = %s", ("Initial Insert",))
    result = new_connection.fetchone()[0]
    assert result == "SUCCESS"

def test_transaction_integrity(create_resilience_table, postgres_connection):
    """Test that incomplete transactions do not persist."""
    cursor = create_resilience_table
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO resilience_tests (test_case, result) VALUES (%s, %s)",
                   ("Uncommitted Transaction", "FAIL"))
    cursor.execute("ROLLBACK")
    
    cursor.execute("SELECT COUNT(*) FROM resilience_tests WHERE test_case = %s", ("Uncommitted Transaction",))
    count = cursor.fetchone()[0]
    assert count == 0  # The rollback should prevent persistence