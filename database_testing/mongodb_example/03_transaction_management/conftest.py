"""
conftest.py - Shared fixtures for MongoDB example
"""

import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with replica set enabled to support transactions."""
    with MongoDbContainer("mongo:6.0").with_command("--replSet rs0") as mongo:
        mongo.start()

        client = MongoClient(mongo.get_connection_url())

        # Wait for MongoDB to become available
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                client.admin.command("ping")
                break
            except ServerSelectionTimeoutError:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(3)  # Wait before retrying
        
        # Initiate the replica set
        try:
            client.admin.command("replSetInitiate")
        except Exception as e:
            print(f"Replica set initiation failed: {e}")

        yield mongo.get_connection_url()


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)

    # Ensure the client can connect before yielding
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            client.admin.command("ping")
            break
        except ServerSelectionTimeoutError:
            if attempt == max_attempts - 1:
                raise
            time.sleep(3)  # Wait before retrying

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


@pytest.fixture(scope="module")
def mongo_session(mongodb_client):
    """Provide a session for MongoDB transactions."""
    session = mongodb_client.start_session()
    yield session
    session.end_session()
