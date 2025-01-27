"""
conftest.py - Shared fixtures for MongoDB resilience testing using Docker API.
"""

import pytest
import time
import docker
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a fixed name to persist across restarts using Docker API."""
    client = docker.from_env()
    
    # Check if container already exists (to prevent multiple creations)
    try:
        container = client.containers.get("mongodb-testcontainer")
        print("♻️ Reusing existing MongoDB container...")
        container.start()
    except docker.errors.NotFound:
        container = client.containers.run(
            "mongo:6.0",
            name="mongodb-testcontainer",
            ports={"27017/tcp": 27017},
            detach=True,
            remove=False,  # Don't auto-remove container
        )
        print("🚀 Starting a new MongoDB container...")

    time.sleep(5)  # Ensure MongoDB initializes properly

    yield container

    print("🛑 Stopping MongoDB container...")
    container.stop()

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
