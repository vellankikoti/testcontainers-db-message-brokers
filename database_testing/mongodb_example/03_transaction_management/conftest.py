"""
conftest.py - Shared fixtures for MongoDB with transactions enabled.
"""

import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly initialized replica set."""
    with MongoDbContainer("mongo:6.0").with_command("--replSet rs0 --bind_ip_all") as mongo:
        mongo.start()
        connection_url = mongo.get_connection_url()
        client = MongoClient(connection_url)

        print("[INFO] Waiting for MongoDB to start...")

        # Ensure MongoDB is accessible
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                client.admin.command("ping")
                print(f"[INFO] MongoDB is responsive. Attempt {attempt + 1}/{max_attempts}")
                break
            except ServerSelectionTimeoutError:
                print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/{max_attempts})...")
                time.sleep(2)

        # Check if the replica set is already initialized
        try:
            status = client.admin.command("replSetGetStatus")
            if status["myState"] == 1:  # PRIMARY node already active
                print("[INFO] MongoDB replica set is already PRIMARY.")
        except OperationFailure:
            print("[INFO] Initiating MongoDB replica set...")
            client.admin.command("replSetInitiate")
            time.sleep(5)  # Wait for replica set to initialize

        # Ensure MongoDB has a PRIMARY node
        for attempt in range(max_attempts):
            try:
                status = client.admin.command("replSetGetStatus")
                if status["myState"] == 1:  # PRIMARY node active
                    print("[INFO] MongoDB replica set is fully initialized with a PRIMARY node.")
                    break
            except OperationFailure:
                print(f"[WARNING] Waiting for MongoDB PRIMARY election ({attempt + 1}/{max_attempts})...")
                time.sleep(2)

            if attempt == max_attempts - 1:
                raise RuntimeError("MongoDB replica set failed to initialize.")

        yield connection_url


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container, retryWrites=False)

    # Ensure MongoDB is accessible
    max_attempts = 20
    for attempt in range(max_attempts):
        try:
            client.admin.command("ping")
            print(f"[INFO] MongoDB client connected. Attempt {attempt + 1}/{max_attempts}")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] Waiting for MongoDB client connection ({attempt + 1}/{max_attempts})...")
            time.sleep(2)

    yield client
    client.close()


@pytest.fixture(scope="module")
def transactions_collection(mongodb_client):
    """Set up the 'transactions' collection in the MongoDB database."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("transactions")

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
