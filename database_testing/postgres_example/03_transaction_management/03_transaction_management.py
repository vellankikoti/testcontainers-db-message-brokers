"""
03_transaction_management.py - Demonstrates transaction management in PostgreSQL with Testcontainers.

This example tests transaction rollback, commit, and isolation.
"""

import pytest
from psycopg2 import DatabaseError

def test_transaction_commit(create_transaction_table, postgres_connection):
    """Test that a committed transaction persists the data."""
    cursor = create_transaction_table
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO transactions (account, amount, status) VALUES (%s, %s, %s) RETURNING id", 
                   ("Alice", 100.50, "COMPLETED"))
    transaction_id = cursor.fetchone()[0]
    cursor.execute("COMMIT")
    
    cursor.execute("SELECT status FROM transactions WHERE id = %s", (transaction_id,))
    status = cursor.fetchone()[0]
    assert status == "COMPLETED"

def test_transaction_rollback(create_transaction_table, postgres_connection):
    """Test that a rolled back transaction does not persist the data."""
    cursor = create_transaction_table
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO transactions (account, amount, status) VALUES (%s, %s, %s) RETURNING id", 
                   ("Bob", 200.75, "PENDING"))
    transaction_id = cursor.fetchone()[0]
    cursor.execute("ROLLBACK")
    
    cursor.execute("SELECT id FROM transactions WHERE id = %s", (transaction_id,))
    result = cursor.fetchone()
    assert result is None

def test_transaction_isolation(create_transaction_table, postgres_connection):
    """Test transaction isolation by running two transactions simultaneously."""
    cursor = create_transaction_table
    connection2 = postgres_connection.cursor()
    
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO transactions (account, amount, status) VALUES (%s, %s, %s) RETURNING id", 
                   ("Charlie", 300.00, "IN_PROGRESS"))
    transaction_id = cursor.fetchone()[0]
    
    connection2.execute("SELECT status FROM transactions WHERE id = %s", (transaction_id,))
    result = connection2.fetchone()
    assert result is None  # Other transaction shouldn't see uncommitted data
    
    cursor.execute("COMMIT")
    connection2.execute("SELECT status FROM transactions WHERE id = %s", (transaction_id,))
    result = connection2.fetchone()
    assert result[0] == "IN_PROGRESS"  # Now committed, should be visible