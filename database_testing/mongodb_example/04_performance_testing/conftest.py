"""
conftest.py - Shared fixtures for MongoDB example
"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container and provide the connection URL."""
    with MongoDbContainer("mongo:6.0") as mongo:
        yield mongo.get_connection_url()

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()

@pytest.fixture(scope="module")
def test_collection(mongodb_client):
    """Set up the 'test_data' collection in the MongoDB database."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("test_data")
    # Ensure the collection is empty before starting tests
    collection.delete_many({})
    yield collection
    # Clean up after tests
    collection.delete_many({})