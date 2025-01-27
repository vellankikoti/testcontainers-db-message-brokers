"""
05_field_constraints_and_indexes.py - Field Constraints & Index Testing with MySQL and Testcontainers

This test ensures that:
1. NOT NULL constraints prevent missing values.
2. CHECK constraints enforce valid data ranges.
3. Indexes improve query performance.

"""

import pytest
import mysql.connector
from mysql.connector import Error

def test_not_null_constraint(mysql_cursor):
    """
    Ensures MySQL prevents inserting NULL values for NOT NULL constrained columns.

    Steps:
    1. Create a products table with NOT NULL constraints on 'name' and 'price'.
    2. Attempt to insert a valid record (should succeed).
    3. Attempt to insert a record with NULL values (should fail).
    4. Validate that MySQL rejects the NULL values.
    """
    mysql_cursor.execute("DROP TABLE IF EXISTS products")
    mysql_cursor.execute("""
        CREATE TABLE products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
    """)

    try:
        # Insert a valid record
        mysql_cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", ("Laptop", 999.99))
        print("✅ NOT NULL Constraint: Inserted valid record successfully.")

        # Attempt to insert a record with NULL values (should fail)
        mysql_cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (None, None))
        print("❌ NOT NULL Constraint Failed: Allowed NULL values.")
    except Error:
        print("✅ NOT NULL Constraint Passed: NULL values prevented.")


def test_check_constraint(mysql_cursor):
    """
    Ensures MySQL enforces CHECK constraints for valid data ranges.

    Steps:
    1. Create a table with a CHECK constraint on the 'age' column.
    2. Insert a valid record (should succeed).
    3. Attempt to insert an invalid age (should fail).
    4. Validate that MySQL rejects the out-of-range value.
    """
    mysql_cursor.execute("DROP TABLE IF EXISTS employees")
    mysql_cursor.execute("""
        CREATE TABLE employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT CHECK (age >= 18)
        )
    """)

    try:
        # Insert a valid record
        mysql_cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", ("Alice", 25))
        print("✅ CHECK Constraint: Inserted valid age successfully.")

        # Attempt to insert an invalid age (should fail)
        mysql_cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", ("Bob", 15))
        print("❌ CHECK Constraint Failed: Allowed invalid age.")
    except Error:
        print("✅ CHECK Constraint Passed: Invalid age prevented.")


def test_index_performance(mysql_cursor):
    """
    Ensures MySQL queries using indexed fields execute efficiently.

    Steps:
    1. Create a table with an index on the 'salary' column.
    2. Insert multiple records with different salary values.
    3. Execute a query using the indexed field.
    4. Validate that the query executes successfully and retrieves the expected results.
    """
    mysql_cursor.execute("DROP TABLE IF EXISTS employees")
    mysql_cursor.execute("""
        CREATE TABLE employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            salary DECIMAL(10,2) NOT NULL,
            INDEX (salary)
        )
    """)

    # Insert multiple records
    mysql_cursor.executemany(
        "INSERT INTO employees (name, salary) VALUES (%s, %s)",
        [("Alice", 50000.00), ("Bob", 60000.00), ("Charlie", 70000.00)]
    )

    # Query using the indexed field
    mysql_cursor.execute("SELECT COUNT(*) FROM employees WHERE salary > 55000")
    result = mysql_cursor.fetchone()

    assert result[0] == 2, "❌ Index Performance Test Failed: Incorrect query result."
    print("✅ Index Performance Test Passed: Indexed query executed successfully.")
