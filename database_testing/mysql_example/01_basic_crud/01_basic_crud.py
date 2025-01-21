"""
01_basic_crud.py - Demonstrates basic CRUD operations with MySQL using Testcontainers.

This example shows how to insert, retrieve, update, and delete records in a MySQL database.
"""

import pytest

def test_create_guest(create_table, mysql_connection):
    """Test creating a new guest."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s)", ("Alice", "alice@example.com", "123-456-7890"))
    mysql_connection.commit()
    
    cursor.execute("SELECT * FROM guests WHERE email = %s", ("alice@example.com",))
    guest = cursor.fetchone()
    assert guest is not None
    assert guest[1] == "Alice"
    assert guest[2] == "alice@example.com"
    assert guest[3] == "123-456-7890"


def test_read_guest(create_table, mysql_connection):
    """Test reading a guest's details."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s)", ("Bob", "bob@example.com", "987-654-3210"))
    mysql_connection.commit()
    
    cursor.execute("SELECT * FROM guests WHERE email = %s", ("bob@example.com",))
    guest = cursor.fetchone()
    assert guest is not None
    assert guest[1] == "Bob"
    assert guest[3] == "987-654-3210"


def test_update_guest(create_table, mysql_connection):
    """Test updating a guest's details."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s)", ("Charlie", "charlie@example.com", "555-555-5555"))
    mysql_connection.commit()
    
    cursor.execute("UPDATE guests SET phone = %s WHERE email = %s", ("111-111-1111", "charlie@example.com"))
    mysql_connection.commit()
    
    cursor.execute("SELECT * FROM guests WHERE email = %s", ("charlie@example.com",))
    updated_guest = cursor.fetchone()
    assert updated_guest[3] == "111-111-1111"


def test_delete_guest(create_table, mysql_connection):
    """Test deleting a guest."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s)", ("Dave", "dave@example.com", "444-444-4444"))
    mysql_connection.commit()
    
    cursor.execute("DELETE FROM guests WHERE email = %s", ("dave@example.com",))
    mysql_connection.commit()
    
    cursor.execute("SELECT * FROM guests WHERE email = %s", ("dave@example.com",))
    deleted_guest = cursor.fetchone()
    assert deleted_guest is None