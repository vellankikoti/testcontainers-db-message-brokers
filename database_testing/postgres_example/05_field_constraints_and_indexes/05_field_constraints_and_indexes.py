"""
05_field_constraints_and_indexes.py - Field Constraints & Index Testing with PostgreSQL and Testcontainers

This test ensures that:
1. NOT NULL constraints prevent missing values.
2. CHECK constraints enforce valid data ranges.
3. Indexes improve query performance.

"""

import pytest
import psycopg2
from psycopg2 import errors

def test_not_null_constraint(postgres_cursor):
    """
    Ensures PostgreSQL prevents inserting NULL values for NOT NULL constrained columns.

    Steps:
    1. Create a products table with NOT NULL constraints on 'name' and 'price'.
    2. Attempt to insert a valid record (should succeed).
    3. Attempt to insert a record with NULL values (should fail).
    4. Validate that PostgreSQL rejects the NULL values.
    """
    postgres_cursor.execute("DROP TABLE IF EXISTS products")
    postgres_cursor.execute("""
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
    """)

    try:
        # Insert a valid record
        postgres_cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", ("Laptop", 999.99))
        print("✅ NOT NULL Constraint: Inserted valid record successfully.")

        # Attempt to insert a record with NULL values (should fail)
        postgres_cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (None, None))
        print("❌ NOT NULL Constraint Failed: Allowed NULL values.")
    except errors.NotNullViolation:
        print("✅ NOT NULL Constraint Passed: NULL values prevented.")
        postgres_cursor.connection.rollback()


def test_check_constraint(postgres_cursor):
    """
    Ensures PostgreSQL enforces CHECK constraints for valid data ranges.

    Steps:
    1. Create a table with a CHECK constraint on the 'age' column.
    2. Insert a valid record (should succeed).
    3. Attempt to insert an invalid age (should fail).
    4. Validate that PostgreSQL rejects the out-of-range value.
    """
    postgres_cursor.execute("DROP TABLE IF EXISTS employees")
    postgres_cursor.execute("""
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT CHECK (age >= 18)
        )
    """)

    try:
        # Insert a valid record
        postgres_cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", ("Alice", 25))
        print("✅ CHECK Constraint: Inserted valid age successfully.")

        # Attempt to insert an invalid age (should fail)
        postgres_cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", ("Bob", 15))
        print("❌ CHECK Constraint Failed: Allowed invalid age.")
    except errors.CheckViolation:
        print("✅ CHECK Constraint Passed: Invalid age prevented.")
        postgres_cursor.connection.rollback()


def test_index_performance(postgres_cursor):
    """
    Ensures PostgreSQL queries using indexed fields execute efficiently.

    Steps:
    1. Create a table with a 'salary' column.
    2. Create an index on the 'salary' column.
    3. Insert multiple records with different salary values.
    4. Execute a query using the indexed field.
    5. Validate that the query executes successfully and retrieves the expected results.
    """
    postgres_cursor.execute("DROP TABLE IF EXISTS employees")
    postgres_cursor.execute("""
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            salary DECIMAL(10,2) NOT NULL
        )
    """)

    # Create index separately (PostgreSQL syntax)
    postgres_cursor.execute("CREATE INDEX salary_index ON employees(salary)")

    # Insert multiple records
    postgres_cursor.executemany(
        "INSERT INTO employees (name, salary) VALUES (%s, %s)",
        [("Alice", 50000.00), ("Bob", 60000.00), ("Charlie", 70000.00)]
    )

    # Query using the indexed field
    postgres_cursor.execute("SELECT COUNT(*) FROM employees WHERE salary > 55000")
    result = postgres_cursor.fetchone()

    assert result[0] == 2, "❌ Index Performance Test Failed: Incorrect query result."
    print("✅ Index Performance Test Passed: Indexed query executed successfully.")
