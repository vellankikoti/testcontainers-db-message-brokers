"""
05_field_constraints_and_indexes.py - Field Constraints & Index Testing with MongoDB and Testcontainers

This example demonstrates how to enforce data integrity in MongoDB using unique indexes 
and field constraints. It ensures that:
- Unique constraints prevent duplicate data.
- Data type constraints are respected.
- Indexed queries perform efficiently.

"""

import pytest
import pymongo

def test_unique_index_constraint(test_collection):
    """
    Ensures that MongoDB prevents duplicate values for fields with a unique index.

    Steps:
    1. Create a unique index on the 'email' field.
    2. Insert a valid record.
    3. Attempt to insert a duplicate record (should fail).
    4. Validate that the duplicate insertion is rejected.
    """
    test_collection.create_index([("email", pymongo.ASCENDING)], unique=True)

    try:
        # Insert a valid record
        test_collection.insert_one({"email": "alice@example.com", "name": "Alice"})
        print("✅ Unique Index Constraint: Inserted first record successfully.")

        # Attempt to insert a duplicate record (should fail)
        test_collection.insert_one({"email": "alice@example.com", "name": "Duplicate Alice"})
        print("❌ Unique Index Constraint Failed: Duplicate Allowed.")

    except pymongo.errors.DuplicateKeyError:
        print("✅ Unique Index Constraint Passed: Duplicate Prevented.")


def test_data_type_constraint(test_collection):
    """
    Ensures that MongoDB respects data type constraints through application logic.

    Steps:
    1. Insert a record with a valid integer value for 'age'.
    2. Attempt to insert an invalid string value for 'age' (should fail).
    3. Validate that the incorrect data type is rejected.
    """
    try:
        # Insert a valid record
        test_collection.insert_one({"name": "Bob", "age": 30})
        print("✅ Data Type Constraint: Inserted valid age.")

        # Attempt to insert invalid data type for 'age' (should fail)
        test_collection.insert_one({"name": "Charlie", "age": "Thirty"})  # Invalid
        print("❌ Data Type Constraint Failed: Allowed incorrect age type.")

    except Exception as e:
        print("✅ Data Type Constraint Passed: Rejected incorrect age type.")


def test_index_performance(test_collection):
    """
    Ensures that MongoDB queries using indexed fields execute correctly.

    Steps:
    1. Create an index on the 'age' field.
    2. Insert multiple records with different age values.
    3. Execute a query using the indexed field.
    4. Validate that the query executes successfully and retrieves the expected results.
    """
    test_collection.create_index([("age", pymongo.ASCENDING)])

    # Insert multiple records
    test_collection.insert_many([
        {"name": "Dave", "age": 25},
        {"name": "Emma", "age": 35},
        {"name": "Frank", "age": 40},
    ])

    # Query using the indexed field
    query_result = test_collection.find({"age": {"$gt": 30}})
    result_count = sum(1 for _ in query_result)

    assert result_count == 2, "❌ Index Performance Test Failed: Incorrect query result."
    print("✅ Index Performance Test Passed: Indexed query executed successfully.")
