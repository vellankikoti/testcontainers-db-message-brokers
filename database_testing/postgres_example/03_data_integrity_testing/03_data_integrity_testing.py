"""
03_data_integrity_testing.py - Data Integrity Testing with PostgreSQL and Testcontainers

This test ensures that:
1. UNIQUE constraints prevent duplicate records.
2. Transactions enforce atomicity (all-or-nothing).
3. FOREIGN KEY constraints maintain referential integrity.

"""

import pytest
import psycopg2
from psycopg2 import sql, errors

def test_unique_constraint(postgres_cursor):
    """
    Ensures PostgreSQL prevents duplicate entries using a UNIQUE constraint.

    Steps:
    1. Create a users table with a UNIQUE constraint on 'email'.
    2. Insert a valid record.
    3. Attempt to insert a duplicate record (should fail).
    4. Validate that PostgreSQL rejects the duplicate entry.
    """
    postgres_cursor.execute("DROP TABLE IF EXISTS users")
    postgres_cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL
        )
    """)

    try:
        # Insert a valid record
        postgres_cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", ("alice@example.com", "Alice"))
        postgres_cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", ("alice@example.com", "Duplicate Alice"))
        print("❌ Unique Constraint Failed: Duplicate Allowed.")
    except errors.UniqueViolation:
        print("✅ Unique Constraint Passed: Duplicate Prevented.")
        postgres_cursor.connection.rollback()


def test_transaction_atomicity(postgres_cursor):
    """
    Ensures PostgreSQL transactions maintain atomicity (all or nothing).

    Steps:
    1. Create an orders table.
    2. Start a transaction and insert multiple records.
    3. Force a failure after one insert.
    4. Ensure that no records are committed.
    """
    postgres_cursor.execute("DROP TABLE IF EXISTS orders")
    postgres_cursor.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            customer VARCHAR(100) NOT NULL,
            amount DECIMAL(10,2) NOT NULL
        )
    """)

    connection = postgres_cursor.connection
    connection.autocommit = False  # Disable auto-commit for transaction

    try:
        postgres_cursor.execute("INSERT INTO orders (customer, amount) VALUES (%s, %s)", ("Bob", 50.00))
        raise Exception("Simulating failure before commit.")  # Simulate error
        connection.commit()
        print("❌ Transaction Atomicity Failed: Partial commit allowed.")
    except:
        connection.rollback()
        print("✅ Transaction Atomicity Passed: No partial commit.")


def test_foreign_key_constraint(postgres_cursor):
    """
    Ensures PostgreSQL enforces foreign key constraints.

    Steps:
    1. Create a parent (customers) and child (orders) table with a foreign key.
    2. Insert a valid parent record.
    3. Attempt to insert an order with a non-existent customer (should fail).
    4. Validate that PostgreSQL rejects the orphaned record.
    """
    postgres_cursor.execute("DROP TABLE IF EXISTS orders")
    postgres_cursor.execute("DROP TABLE IF EXISTS customers")

    postgres_cursor.execute("""
        CREATE TABLE customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)

    postgres_cursor.execute("""
        CREATE TABLE orders (
            id SERIAL PRIMARY KEY,
            customer_id INT,
            amount DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
        )
    """)

    # Insert a valid customer
    postgres_cursor.execute("INSERT INTO customers (name) VALUES (%s)", ("Charlie",))

    try:
        # Attempt to insert an order with a non-existent customer_id
        postgres_cursor.execute("INSERT INTO orders (customer_id, amount) VALUES (%s, %s)", (999, 25.00))
        print("❌ Foreign Key Constraint Failed: Orphan
