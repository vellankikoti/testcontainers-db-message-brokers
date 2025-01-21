"""
01_basic_crud.py - Demonstrates basic CRUD operations in PostgreSQL with Testcontainers.

This example tests inserting, reading, updating, and deleting records from a PostgreSQL table.
"""

import pytest

def test_create_guest(create_table, postgres_connection):
    """Test creating a new guest."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s) RETURNING id", 
                   ("Alice", "alice@example.com", "123-456-7890"))
    guest_id = cursor.fetchone()[0]
    postgres_connection.commit()
    assert guest_id is not None

def test_read_guest(create_table, postgres_connection):
    """Test reading a guest's details."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s) RETURNING id", 
                   ("Bob", "bob@example.com", "987-654-3210"))
    guest_id = cursor.fetchone()[0]
    postgres_connection.commit()
    
    cursor.execute("SELECT name, email, phone FROM guests WHERE id = %s", (guest_id,))
    saved_guest = cursor.fetchone()
    assert saved_guest == ("Bob", "bob@example.com", "987-654-3210")

def test_update_guest(create_table, postgres_connection):
    """Test updating a guest's details."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s) RETURNING id", 
                   ("Charlie", "charlie@example.com", "555-555-5555"))
    guest_id = cursor.fetchone()[0]
    postgres_connection.commit()
    
    cursor.execute("UPDATE guests SET phone = %s WHERE id = %s", ("111-111-1111", guest_id))
    postgres_connection.commit()
    
    cursor.execute("SELECT phone FROM guests WHERE id = %s", (guest_id,))
    updated_phone = cursor.fetchone()[0]
    assert updated_phone == "111-111-1111"

def test_delete_guest(create_table, postgres_connection):
    """Test deleting a guest."""
    cursor = create_table
    cursor.execute("INSERT INTO guests (name, email, phone) VALUES (%s, %s, %s) RETURNING id", 
                   ("Dave", "dave@example.com", "444-444-4444"))
    guest_id = cursor.fetchone()[0]
    postgres_connection.commit()
    
    cursor.execute("DELETE FROM guests WHERE id = %s", (guest_id,))
    postgres_connection.commit()
    
    cursor.execute("SELECT id FROM guests WHERE id = %s", (guest_id,))
    deleted_guest = cursor.fetchone()
    assert deleted_guest is None