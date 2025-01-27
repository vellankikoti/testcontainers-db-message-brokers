"""
conftest.py - Shared fixtures for MongoDB resilience testing.
"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container and return the container object."""
    with MongoDbContainer("mongo:6.0") as mongo:
        yield mongo  # ✅ Return full container object (not just URL)

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container.get_connection_url())  # ✅ Correct usage of connection URL
    yield client
    client.close()

@pytest.fixture(scope="module")
def test_collection(mongodb_client):
    """Set up a dedicated test collection for resilience testing."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("resilience_test")

    # Cleanup before and after tests
    collection.delete_many({})
    yield collection
    collection.delete_many({})
