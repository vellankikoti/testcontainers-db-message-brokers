"""
conftest.py - Shared fixtures for MongoDB resilience testing.
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with proper lifecycle management."""
    with DockerContainer("mongo:6.0") \
            .with_bind_ports(27017, 27017) as mongo:
        print("🚀 Starting MongoDB container with fixed lifecycle...")
        time.sleep(5)  # Ensures MongoDB initializes properly
        yield mongo  # ✅ Returning full container instance

@pytest.fixture(scope="function")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    mongo_url = f"mongodb://localhost:27017"  # Explicitly set localhost port

    # Ensure MongoDB is responsive before proceeding
    for _ in range(5):
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
            client.server_info()  # Test connection
            yield client
            client.close()
            return
        except Exception:
            time.sleep(2)  # Retry every 2 seconds if connection fails

    pytest.fail("❌ MongoDB did not start within the expected time!")

@pytest.fixture(scope="function")
def test_collection(mongodb_client):
    """Set up a dedicated test collection for resilience testing."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("resilience_test")

    # Cleanup before and after tests
    collection.delete_many({})
    yield collection
    collection.delete_many({})
