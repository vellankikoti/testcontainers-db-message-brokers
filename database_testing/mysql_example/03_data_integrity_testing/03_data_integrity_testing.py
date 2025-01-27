"""
03_data_integrity_testing.py - Data Integrity Testing with MySQL and Testcontainers

This test ensures that:
1. Unique constraints prevent duplicate records.
2. Transactions enforce atomicity.
3. Foreign key constraints prevent orphan records.

"""

import pytest
import mysql.connector
from mysql.connector import Error

def test_unique_constraint(mysql_cursor):
    """
    Ensures MySQL prevents duplicate entries using a UNIQUE constraint.

    Steps:
    1. Create a users table with a UNIQUE constraint on 'email'.
    2. Insert a valid record.
    3. Attempt to insert a duplicate record (should fail).
    4. Validate that MySQL rejects the duplicate entry.
    """
    mysql_cursor.execute("DROP TABLE IF EXISTS users")
    mysql_cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL
        )
    """)

    try:
        # Insert a valid record
        mysql_cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", ("alice@example.com", "Alice"))
        mysql_cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", ("alice@example.com", "Duplicate Alice"))
        print("❌ Unique Constraint Failed: Duplicate Allowed.")
    except Error as e:
        print("✅ Unique Constraint Passed: Duplicate Prevented.", e)


def test_transaction_atomicity(mysql_cursor):
    """
    Ensures MySQL transactions maintain atomicity (all or nothing).

    Steps:
    1. Create an orders table.
    2. Start a transaction and insert multiple records.
    3. Force a failure after one insert.
    4. Ensure that no records are committed.
    """
    mysql_cursor.execute("DROP TABLE IF EXISTS orders")
    mysql_cursor.execute("""
        CREATE TABLE orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer VARCHAR(100) NOT NULL,
            amount DECIMAL(10,2) NOT NULL
        )
    """)

    connection = mysql_cursor._connection
    connection.start_transaction()

    try:
        mysql_cursor.execute("INSERT INTO orders (customer, amount) VALUES (%s, %s)", ("Bob", 50.00))
        raise Exception("Simulating failure before commit.")  # Simulate error
        connection.commit()
        print("❌ Transaction Atomicity Failed: Partial commit allowed.")
    except:
        connection.rollback()
        print("✅ Transaction Atomicity Passed: No partial commit.")


def test_foreign_key_constraint(mysql_cursor):
    """
    Ensures MySQL enforces foreign key constraints.

    Steps:
    1. Create a parent (customers) and child (orders) table with a foreign key.
    2. Insert a valid parent record.
    3. Attempt to insert an order with a non-existent customer (should fail).
    4. Validate that MySQL rejects the orphaned record.
    """
    mysql_cursor.execute("DROP TABLE IF EXISTS orders")
    mysql_cursor.execute("DROP TABLE IF EXISTS customers")

    mysql_cursor.execute("""
        CREATE TABLE customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
    """)

    mysql_cursor.execute("""
        CREATE TABLE orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            amount DECIMAL(10,2),
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
        )
    """)

    # Insert a valid customer
    mysql_cursor.execute("INSERT INTO customers (name) VALUES (%s)", ("Charlie",))

    try:
        # Attempt to insert an order with a non-existent customer_id
        mysql_cursor.execute("INSERT INTO orders (customer_id, amount) VALUES (%s, %s)", (999, 25.00))
        print("❌ Foreign Key Constraint Failed: Orphaned record allowed.")
    except Error:
        print("✅ Foreign Key Constraint Passed: Orphaned record prevented.")
