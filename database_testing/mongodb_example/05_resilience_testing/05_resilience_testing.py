"""
05_resilience_testing.py - Demonstrates resilience testing in MongoDB with Testcontainers.

This example simulates MongoDB failures, verifies automatic recovery, and ensures data integrity.
"""

import pytest
import time
from pymongo.errors import ConnectionFailure

@pytest.mark.resilience
def test_mongodb_reconnect(mongodb_client, mongodb_container, test_collection):
    """Test MongoDB automatic reconnection after failure."""
    
    # Insert initial test data
    test_collection.insert_one({"status": "initial"})

    # Ensure data is present before failure
    assert test_collection.find_one({"status": "initial"}) is not None

    # Stop MongoDB container to simulate failure
    print("🛑 Stopping MongoDB container...")
    mongodb_container.stop()
    time.sleep(5)  # Give time for the stop to take effect

    # Attempt reconnection (should fail)
    with pytest.raises(ConnectionFailure):
        mongodb_client.server_info()  # Explicitly checking connection failure

    # Restart MongoDB container
    print("🚀 Restarting MongoDB container...")
    mongodb_container.start()
    time.sleep(5)  # Wait for MongoDB to restart

    # Retry reconnection logic (up to 10 seconds)
    for attempt in range(10):
        try:
            mongodb_client.server_info()
            print(f"✅ MongoDB reconnected successfully after {attempt + 1} seconds")
            break
        except ConnectionFailure:
            print(f"🔄 Retrying connection... Attempt {attempt + 1}")
            time.sleep(1)
    else:
        pytest.fail("❌ MongoDB did not restart successfully!")

    # Verify data integrity
    assert test_collection.find_one({"status": "initial"}) is not None, "❌ Data was lost after restart!"

    # Insert new record post-recovery
    test_collection.insert_one({"status": "recovered"})

    # Validate both records exist
    assert test_collection.count_documents({}) == 2, "❌ Incorrect number of records after recovery!"
