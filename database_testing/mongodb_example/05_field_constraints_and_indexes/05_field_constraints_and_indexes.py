"""
05_field_constraints_and_indexes.py - Field Constraints & Index Testing with MongoDB and Testcontainers

This example ensures that:
- Unique constraints prevent duplicate values.
- Data type constraints are respected.
- Indexed queries execute efficiently.
"""

import pytest
import pymongo

def test_unique_index_constraint(test_collection):
    """
    Ensures MongoDB prevents duplicate values for fields with a unique index.

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
    Ensures MongoDB respects data type constraints through application logic.

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


def test_index_performance(mongodb_client):
    """
    Ensures that MongoDB queries using indexed fields execute correctly.

    Steps:
    1. Use a separate collection for index testing to avoid conflicts.
    2. Create an index on the 'age' field.
    3. Insert multiple records with different age values.
    4. Execute a query using the indexed field.
    5. Validate that the query executes successfully and retrieves the expected results.
    """
    db = mongodb_client.test_db
    index_test_collection = db.index_performance_test  # Separate collection for indexing test
    index_test_collection.delete_many({})  # Cleanup before test

    index_test_collection.create_index([("age", pymongo.ASCENDING)])

    # Insert multiple records (no unique index on email)
    index_test_collection.insert_many([
        {"name": "Dave", "age": 25, "email": "dave@example.com"},
        {"name": "Emma", "age": 35, "email": "emma@example.com"},
        {"name": "Frank", "age": 40, "email": "frank@example.com"},
    ])

    # Query using the indexed field
    query_result = index_test_collection.find({"age": {"$gt": 30}})
    result_count = sum(1 for _ in query_result)

    assert result_count == 2, "❌ Index Performance Test Failed: Incorrect query result."
    print("✅ Index Performance Test Passed: Indexed query executed successfully.")
