"""
03_transaction_management.py - Demonstrates transaction management in MySQL with Testcontainers.

This example ensures that MySQL transactions follow ACID properties, such as rollback on failure.
"""

import pytest
from mysql.connector import Error

def test_transaction_commit(create_table, mysql_connection):
    """Test that a transaction is committed properly."""
    cursor = create_table
    try:
        mysql_connection.start_transaction()
        cursor.execute("INSERT INTO transactions (account, amount) VALUES (%s, %s)", ("Alice", 100.00))
        cursor.execute("INSERT INTO transactions (account, amount) VALUES (%s, %s)", ("Bob", 200.00))
        mysql_connection.commit()
    except Error:
        mysql_connection.rollback()
    
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    assert count == 2


def test_transaction_rollback(create_table, mysql_connection):
    """Test that a transaction is rolled back on error."""
    cursor = create_table
    try:
        mysql_connection.start_transaction()
        cursor.execute("INSERT INTO transactions (account, amount) VALUES (%s, %s)", ("Charlie", 300.00))
        cursor.execute("INSERT INTO transactions (account, amount) VALUES (%s, %s)", ("Dave", 'INVALID_AMOUNT'))  # Intentional error
        mysql_connection.commit()
    except Error:
        mysql_connection.rollback()
    
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    assert count == 0  # Rollback should prevent insertions