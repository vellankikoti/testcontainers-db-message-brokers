"""
05_resilience_testing.py - Demonstrates resilience testing in MongoDB with Testcontainers.

This example shows how to handle MongoDB failures, simulate downtime, and ensure automatic recovery.
"""

import pytest
import time
from pymongo.errors import ConnectionFailure

@pytest.mark.resilience
def test_mongodb_reconnect(mongodb_client, mongodb_container, test_collection):
    """Test MongoDB automatic reconnection after failure."""
    
    # Insert initial test data
    test_collection.insert_one({"status": "initial"})
    
    # Verify data is present
    assert test_collection.find_one({"status": "initial"}) is not None

    # Stop MongoDB container to simulate failure
    mongodb_container.stop()
    time.sleep(5)

    # Attempt to reconnect (should fail)
    with pytest.raises(ConnectionFailure):
        mongodb_client.server_info()  # Explicit connection check

    # Restart MongoDB container
    mongodb_container.start()
    time.sleep(5)

    # Wait for reconnection
    for _ in range(5):  # Retry for up to 5 seconds
        try:
            mongodb_client.server_info()  # Explicit reconnection check
            break
        except ConnectionFailure:
            time.sleep(1)

    # Ensure the database reconnects and data is intact
    assert test_collection.find_one({"status": "initial"}) is not None

    # Insert a new record after recovery
    test_collection.insert_one({"status": "recovered"})

    # Verify both records exist
    assert test_collection.count_documents({}) == 2
