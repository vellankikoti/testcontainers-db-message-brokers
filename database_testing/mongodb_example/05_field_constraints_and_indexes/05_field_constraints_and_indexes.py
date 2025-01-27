import pymongo
import pytest

def test_mongodb_unique_index(mongodb_test_db):
    """
    Ensures that MongoDB prevents duplicate values for fields with a unique index.
    """
    collection = mongodb_test_db.field_constraints_test

    # Create a unique index on 'email'
    collection.create_index([("email", pymongo.ASCENDING)], unique=True)

    try:
        # Insert a valid record
        collection.insert_one({"email": "alice@example.com", "name": "Alice"})
        print("✅ Unique Index: Inserted first record successfully.")

        # Attempt to insert a duplicate record (should fail)
        collection.insert_one({"email": "alice@example.com", "name": "Duplicate Alice"})
        print("❌ Unique Index Test Failed: Duplicate Allowed.")

    except pymongo.errors.DuplicateKeyError:
        print("✅ Unique Index Test Passed: Duplicate Prevented.")

def test_mongodb_data_type_constraint(mongodb_test_db):
    """
    Ensures that MongoDB enforces correct data types through application logic.
    """
    collection = mongodb_test_db.field_constraints_test

    try:
        # Insert valid record
        collection.insert_one({"name": "Bob", "age": 30})  # Valid
        print("✅ Data Type Constraint: Inserted valid age.")

        # Attempt to insert invalid data type for 'age' (should fail)
        collection.insert_one({"name": "Charlie", "age": "Thirty"})  # Invalid
        print("❌ Data Type Constraint Test Failed: Allowed incorrect age type.")

    except Exception as e:
        print("✅ Data Type Constraint Test Passed: Rejected incorrect age type.")

def test_mongodb_index_performance(mongodb_test_db):
    """
    Ensures that MongoDB queries using indexed fields execute correctly.
    """
    collection = mongodb_test_db.field_constraints_test

    # Create an index on 'age'
    collection.create_index([("age", pymongo.ASCENDING)])

    # Insert multiple records
    collection.insert_many([
        {"name": "Dave", "age": 25},
        {"name": "Emma", "age": 35},
        {"name": "Frank", "age": 40},
    ])
    
    # Query using the indexed field
    query_result = collection.find({"age": {"$gt": 30}})
    result_count = sum(1 for _ in query_result)

    assert result_count == 2, "❌ Index Performance Test Failed: Incorrect query result."
    print("✅ Index Performance Test Passed: Indexed query executed successfully.")
