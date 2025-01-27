"""
05_resilience_testing.py - Demonstrates resilience testing in MongoDB with Testcontainers.

This example simulates MongoDB failures, verifies automatic recovery, and ensures data integrity.
"""

import pytest
import time
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

    # Stop MongoDB container to simulate failure
    print("🛑 Stopping MongoDB container...")
    mongodb_container.stop()
    time.sleep(5)

    # Restart MongoDB container
    print("🚀 Restarting MongoDB container...")
    mongodb_container.start()
    time.sleep(5)

    # Create a new MongoDB client after restart
    print("🔄 Reconnecting to MongoDB...")
    new_client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    new_db = new_client.get_database("test_db")
    new_collection = new_db.get_collection("resilience_test")

    # Ensure MongoDB has restarted properly
    for attempt in range(10):
        try:
            new_client.server_info()
            print(f"✅ MongoDB reconnected successfully after {attempt + 1} seconds")
            break
        except ConnectionFailure:
            print(f"🔄 Retrying connection... Attempt {attempt + 1}")
            time.sleep(1)
    else:
        pytest.fail("❌ MongoDB did not restart successfully!")

    # Verify data integrity
    retrieved_data = new_collection.find_one({"status": "initial"})
    assert retrieved_data is not None, "❌ Data was lost after restart!"
    print("✅ Data is still available after restart.")

    # Insert new record post-recovery
    new_collection.insert_one({"status": "recovered"})

    # Validate both records exist
    total_records = new_collection.count_documents({})
    assert total_records == 2, f"❌ Expected 2 records, found {total_records} after recovery!"
    print("✅ Successfully inserted data after recovery, test passed! 🎉")
