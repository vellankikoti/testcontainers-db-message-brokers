"""
conftest.py - Shared fixtures for MongoDB example
"""

import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a replica set to support transactions."""
    with MongoDbContainer("mongo:6.0").with_command("--replSet rs0 --bind_ip_all") as mongo:
        mongo.start()
        connection_url = mongo.get_connection_url()
        client = MongoClient(connection_url)

        # Wait for MongoDB to become available
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                client.admin.command("ping")
                print(f"[INFO] MongoDB is ready. Attempt {attempt + 1}/{max_attempts}")
                break
            except ServerSelectionTimeoutError:
                print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/{max_attempts})...")
                if attempt == max_attempts - 1:
                    raise
                time.sleep(3)

        # Initiate the replica set
        try:
            print("[INFO] Initiating MongoDB replica set...")
            client.admin.command("replSetInitiate")
            time.sleep(5)  # Wait for replica set to initialize
        except OperationFailure as e:
            print(f"[ERROR] Replica set initiation failed: {e}")

        # Verify replica set status
        for attempt in range(max_attempts):
            try:
                status = client.admin.command("replSetGetStatus")
                if status["ok"]:
                    print("[INFO] MongoDB replica set is initialized successfully.")
                    break
            except OperationFailure:
                print(f"[WARNING] Waiting for MongoDB replica set to be ready ({attempt + 1}/{max_attempts})...")
                time.sleep(3)
            if attempt == max_attempts - 1:
                raise RuntimeError("MongoDB replica set failed to initialize.")

        yield connection_url


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)

    # Ensure MongoDB is ready
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            client.admin.command("ping")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] Waiting for MongoDB client connection ({attempt + 1}/{max_attempts})...")
            if attempt == max_attempts - 1:
                raise
            time.sleep(3)

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
