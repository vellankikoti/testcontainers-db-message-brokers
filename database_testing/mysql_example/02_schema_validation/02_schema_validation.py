"""
02_schema_validation.py - Demonstrates schema validation in MySQL with Testcontainers.

This example ensures that MySQL enforces constraints such as uniqueness, NOT NULL, and CHECK constraints.
"""

import pytest
from mysql.connector.errors import IntegrityError

def test_unique_constraint(create_table, mysql_connection):
    """Test that MySQL enforces the UNIQUE constraint on the email field."""
    cursor = create_table
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Alice", "alice@example.com", 30))
    mysql_connection.commit()
    
    with pytest.raises(IntegrityError):
        cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Bob", "alice@example.com", 25))
        mysql_connection.commit()


def test_not_null_constraint(create_table, mysql_connection):
    """Test that MySQL enforces NOT NULL constraint on required fields."""
    cursor = create_table
    with pytest.raises(IntegrityError):
        cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (None, "charlie@example.com", 28))
        mysql_connection.commit()


def test_check_constraint(create_table, mysql_connection):
    """Test that MySQL enforces CHECK constraint on age (must be > 0)."""
    cursor = create_table
    with pytest.raises(IntegrityError):
        cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", ("Dave", "dave@example.com", -5))
        mysql_connection.commit()