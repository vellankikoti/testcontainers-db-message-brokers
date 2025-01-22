"""
conftest.py - Shared fixtures for MongoDB with transaction support.
"""

import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly initialized replica set."""
    with MongoDbContainer("mongo:6.0").with_command("--replSet rs0 --bind_ip_all") as mongo:
        mongo.start()
        connection_url = mongo.get_connection_url()
        client = MongoClient(connection_url)

        print("[INFO] Waiting for MongoDB to start...")

        # Ensure MongoDB is fully started before proceeding
        max_attempts = 20
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
            time.sleep(5)  # Wait for the replica set to initialize
        except OperationFailure as e:
            print(f"[WARNING] Replica set already initialized or failed: {e}")

        # Wait for primary election
        for attempt in range(max_attempts):
            try:
                status = client.admin.command("replSetGetStatus")
                if status["myState"] == 1:  # myState 1 = PRIMARY
                    print("[INFO] MongoDB replica set is fully initialized with a primary node.")
                    break
            except OperationFailure:
                print(f"[WARNING] Waiting for MongoDB primary election ({attempt + 1}/{max_attempts})...")
                time.sleep(3)

            if attempt == max_attempts - 1:
                raise RuntimeError("MongoDB replica set failed to initialize.")

        yield connection_url


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container, retryWrites=False)

    # Ensure MongoDB is responsive before proceeding
    max_attempts = 20
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
