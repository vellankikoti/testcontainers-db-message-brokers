"""
conftest.py - Shared fixtures for MongoDB resilience testing.
"""

import pytest
import time
from testcontainers.core.container import DockerContainer
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with persistent storage."""
    with DockerContainer("mongo:6.0") as mongo:
        mongo.with_bind_ports(27017, 27017)
        mongo.with_volume("/data/db")  # Ensure data persistence
        print("🚀 Starting MongoDB container...")
        mongo.start()
        time.sleep(5)  # Wait for MongoDB to initialize
        yield mongo
        print("🛑 Stopping MongoDB container...")
        mongo.stop()

@pytest.fixture(scope="function")
def mongodb_client():
    """Create a MongoDB client connected to the container."""
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    yield client
    client.close()

@pytest.fixture(scope="function")
def test_collection(mongodb_client):
    """Set up the 'resilience_test' collection in the MongoDB database."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("resilience_test")
    # Ensure the collection is empty before starting tests
    collection.delete_many({})
    yield collection
    # Clean up after tests
    collection.delete_many({})
