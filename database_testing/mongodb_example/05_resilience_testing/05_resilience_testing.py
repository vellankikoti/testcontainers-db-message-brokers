"""
05_resilience_testing.py - Demonstrates resilience testing in MongoDB with Docker API.

This example simulates MongoDB failures, verifies automatic recovery, and ensures data integrity.
"""

import pytest
import time
import docker
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

@pytest.mark.resilience
def test_mongodb_reconnect(mongodb_container, test_collection):
    """Test MongoDB automatic reconnection after failure."""

    # Insert initial test data
    test_collection.insert_one({"status": "initial"})
    print("✅ Inserted initial data before failure.")

    # Ensure data is present before failure
    assert test_collection.find_one({"status": "initial"}) is not None

    # Simulate failure by pausing instead of stopping
    print("🛑 Pausing MongoDB container...")
    client = docker.from_env()
    container = client.containers.get("mongodb-testcontainer")
    container.pause()
    time.sleep(5)

    # Unpause MongoDB container
    print("🚀 Unpausing MongoDB container...")
    container.unpause()
    time.sleep(5)

    # Ensure MongoDB is fully ready after restart
    print("🔄 Reconnecting to MongoDB...")
    mongo_url = "mongodb://localhost:27017"

    for attempt in range(10):
        try:
            new_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            new_client.server_info()
            print(f"✅ MongoDB reconnected successfully after {attempt + 1} seconds")
            break
        except ConnectionFailure:
            print(f"🔄 Retrying connection... Attempt {attempt + 1}")
            time.sleep(1)
    else:
        pytest.fail("❌ MongoDB did not restart successfully!")

    # Create a new MongoDB client and validate data integrity
    new_db = new_client.get_database("test_db")
    new_collection = new_db.get_collection("resilience_test")

    retrieved_data = new_collection.find_one({"status": "initial"})
    assert retrieved_data is not None, "❌ Data was lost after restart!"
    print("✅ Data is still available after restart.")

    # Insert new record post-recovery
    new_collection.insert_one({"status": "recovered"})

    # Validate both records exist
    total_records = new_collection.count_documents({})
    assert total_records == 2, f"❌ Expected 2 records, found {total_records} after recovery!"
    print("✅ Successfully inserted data after recovery, test passed! 🎉")


@pytest.mark.resilience
def test_mongodb_bulk_insert_reconnect(mongodb_container, test_collection):
    """Test MongoDB bulk insert and reconnection after failure."""

    # Insert large volume of data
    bulk_data = [{"user_id": i, "name": f"User{i}"} for i in range(10000)]
    test_collection.insert_many(bulk_data)
    print("✅ Inserted 10,000 documents before failure.")

    # Ensure bulk data exists
    assert test_collection.count_documents({}) == 10000

    # Pause MongoDB container to simulate failure
    print("🛑 Pausing MongoDB container...")
    client = docker.from_env()
    container = client.containers.get("mongodb-testcontainer")
    container.pause()
    time.sleep(5)

    # Unpause MongoDB container
    print("🚀 Unpausing MongoDB container...")
    container.unpause()
    time.sleep(5)

    # Reconnect MongoDB client
    print("🔄 Reconnecting to MongoDB...")
    mongo_url = "mongodb://localhost:27017"

    for attempt in range(10):
        try:
            new_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            new_client.server_info()
            break
        except ConnectionFailure:
            time.sleep(1)
    else:
        pytest.fail("❌ MongoDB did not restart successfully!")

    # Validate all documents are still present
    new_db = new_client.get_database("test_db")
    new_collection = new_db.get_collection("resilience_test")
    assert new_collection.count_documents({}) == 10000, "❌ Data was lost after restart!"
    print("✅ Bulk insert data is intact after restart.")


@pytest.mark.resilience
def test_mongodb_query_after_restart(mongodb_container, test_collection):
    """Test MongoDB complex queries after restart."""

    # Insert sample data
    sample_data = [
        {"user_id": 1, "name": "Alice", "age": 30},
        {"user_id": 2, "name": "Bob", "age": 25},
        {"user_id": 3, "name": "Charlie", "age": 35},
        {"user_id": 4, "name": "David", "age": 40},
    ]
    test_collection.insert_many(sample_data)
    print("✅ Inserted user data before failure.")

    # Pause MongoDB container to simulate failure
    print("🛑 Pausing MongoDB container...")
    client = docker.from_env()
    container = client.containers.get("mongodb-testcontainer")
    container.pause()
    time.sleep(5)

    # Unpause MongoDB container
    print("🚀 Unpausing MongoDB container...")
    container.unpause()
    time.sleep(5)

    # Reconnect MongoDB client
    print("🔄 Reconnecting to MongoDB...")
    mongo_url = "mongodb://localhost:27017"

    for attempt in range(10):
        try:
            new_client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            new_client.server_info()
            break
        except ConnectionFailure:
            time.sleep(1)
    else:
        pytest.fail("❌ MongoDB did not restart successfully!")

    # Validate complex query still works
    new_db = new_client.get_database("test_db")
    new_collection = new_db.get_collection("resilience_test")
    users_above_30 = list(new_collection.find({"age": {"$gt": 30}}))
    
    assert len(users_above_30) == 2, f"❌ Expected 2 users above age 30, but found {len(users_above_30)}"
    print("✅ Query worked correctly after restart.")
