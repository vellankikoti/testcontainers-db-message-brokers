"""
05_resilience_testing.py - Demonstrates resilience testing in MongoDB with Testcontainers.

This example shows how to handle MongoDB failures, simulate downtime, and ensure automatic recovery.
"""

import pytest
import time
from pymongo.errors import ConnectionFailure

def test_mongodb_reconnect(mongodb_client, mongodb_container):
    """Test MongoDB automatic reconnection after failure."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("resilience_test")
    collection.insert_one({"status": "initial"})
    
    # Stop MongoDB container to simulate failure
    mongodb_container.stop()
    time.sleep(5)
    
    # Attempt to reconnect (should fail)
    with pytest.raises(ConnectionFailure):
        collection.find_one()
    
    # Restart MongoDB container
    mongodb_container.start()
    time.sleep(5)
    
    # Verify reconnection
    assert collection.find_one({"status": "initial"}) is not None