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
    mongodb_container.stop()
    time.sleep(5)

    # Attempt reconnection (should fail)
    with pytest.raises(ConnectionFailure):
        mongodb_client.server_info()  # ✅ Explicit connection failure check

    # Restart MongoDB container
    mongodb_container.start()
    time.sleep(5)

    # Ensure MongoDB has restarted properly
    for _ in range(5):
        try:
            mongodb_client.server_info()  # ✅ Test if MongoDB is back online
            break
        except ConnectionFailure:
            time.sleep(1)  # Retry up to 5 seconds

    # Verify data integrity
    assert test_collection.find_one({"status": "initial"}) is not None

    # Insert new record post-recovery
    test_collection.insert_one({"status": "recovered"})

    # Validate both records exist
    assert test_collection.count_documents({}) == 2
