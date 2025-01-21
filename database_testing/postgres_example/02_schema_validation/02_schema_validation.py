"""
02_schema_validation.py - Demonstrates schema validation in PostgreSQL with Testcontainers.

This example tests unique constraints, data type enforcement, and check constraints.
"""

import pytest
from psycopg2 import IntegrityError, DataError

def test_unique_constraint(create_schema, postgres_connection):
    """Test that unique constraint on username is enforced."""
    cursor = create_schema
    cursor.execute("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                   ("alice", "alice@example.com", 25))
    postgres_connection.commit()
    
    with pytest.raises(IntegrityError):
        cursor.execute("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                       ("alice", "alice2@example.com", 30))
        postgres_connection.commit()

def test_check_constraint(create_schema, postgres_connection):
    """Test that the check constraint on age is enforced."""
    cursor = create_schema
    with pytest.raises(DataError):
        cursor.execute("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                       ("bob", "bob@example.com", 15))
        postgres_connection.commit()

def test_email_uniqueness(create_schema, postgres_connection):
    """Test that the email field enforces uniqueness."""
    cursor = create_schema
    cursor.execute("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                   ("charlie", "charlie@example.com", 28))
    postgres_connection.commit()
    
    with pytest.raises(IntegrityError):
        cursor.execute("INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
                       ("charlie2", "charlie@example.com", 30))
        postgres_connection.commit()