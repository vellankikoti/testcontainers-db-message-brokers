"""
conftest.py - Shared fixtures for MongoDB with replica set support.
"""

import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with replica set and ensure readiness."""
    with MongoDbContainer("mongo:6.0").with_command("--replSet rs0 --bind_ip_all") as mongo:
        mongo.start()
        connection_url = mongo.get_connection_url()
        client = MongoClient(connection_url)

        # Ensure MongoDB is fully started before proceeding
        max_attempts = 15
        for attempt in range(max_attempts):
            try:
                client.admin.command("ping")
                print(f"[INFO] MongoDB is ready. Attempt {attempt + 1}/{max_attempts}")
                break
            except ServerSelectionTimeoutError:
                print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/{max_attempts})...")
                time.sleep(3)

        # Initiate replica set (Only needed for transactions)
        try:
            print("[INFO] Initiating MongoDB replica set...")
            client.admin.command("replSetInitiate")
            time.sleep(5)  # Wait for replica set to initialize
        except OperationFailure as e:
            print(f"[WARNING] Replica set already initialized or failed: {e}")

        # Verify replica set is ready
        for attempt in range(max_attempts):
            try:
                status = client.admin.command("replSetGetStatus")
                if status["ok"]:
                    print("[INFO] MongoDB replica set initialized successfully.")
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

    # Ensure MongoDB is responsive before proceeding
    max_attempts = 15
    for attempt in range(max_attempts):
        try:
            client.admin.command("ping")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] Waiting for MongoDB client connection ({attempt + 1}/{max_attempts})...")
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
