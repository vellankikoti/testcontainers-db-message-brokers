"""
conftest.py - Shared fixtures for MongoDB resilience testing.
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a fixed name to persist across restarts."""
    mongo = DockerContainer("mongo:6.0") \
        .with_bind_ports(27017, 27017) \
        .with_name("mongodb-testcontainer")  # Ensure the same container is reused

    print("🚀 Starting MongoDB container...")
    mongo.start()
    time.sleep(5)  # Ensure MongoDB initializes properly
    yield mongo  # Provide container instance for tests
    print("🛑 Stopping MongoDB container...")
    mongo.stop()

@pytest.fixture(scope="function")
def mongodb_client():
    """Create a fresh MongoDB client connection after container restart."""
    mongo_url = "mongodb://localhost:27017"
    for _ in range(10):
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            client.server_info()  # Test connection
            yield client
            client.close()
            return
        except Exception:
            print("🔄 Waiting for MongoDB to become available...")
            time.sleep(2)

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
