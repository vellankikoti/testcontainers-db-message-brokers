"""
conftest.py - Pytest Fixtures for MongoDB Testcontainers

This file sets up a temporary MongoDB container using Testcontainers.
It provides reusable fixtures for MongoDB connections and collections.
"""

import pytest
import pymongo
from testcontainers.mongodb import MongoDbContainer

@pytest.fixture(scope="session")
def mongodb_container():
    """
    Starts a MongoDB Testcontainer before running tests.

    Yields:
    - MongoDB container instance
    """
    container = MongoDbContainer("mongo:latest")
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="session")
def mongodb_client(mongodb_container):
    """
    Provides a MongoDB client connected to the running Testcontainer.

    Yields:
    - pymongo.MongoClient instance
    """
    mongo_uri = mongodb_container.get_connection_url()
    client = pymongo.MongoClient(mongo_uri)
    yield client
    client.close()

@pytest.fixture(scope="function")
def test_collection(mongodb_client):
    """
    Provides a test database and collection, ensuring clean data for each test.

    Yields:
    - MongoDB collection instance for constraint and index testing.
    """
    db = mongodb_client.test_db
    collection = db.field_constraints_test
    collection.delete_many({})  # Cleanup before each test
    yield collection
