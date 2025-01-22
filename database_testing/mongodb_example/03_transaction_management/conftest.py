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
    """Start a MongoDB container with a replica set and wait for it to be ready."""
    mongo = MongoDbContainer("mongo:6.0").with_command("--replSet rs0 --bind_ip_all")
    mongo.start()

    client = MongoClient(mongo.get_connection_url())

    # Wait for MongoDB to be responsive
    for attempt in range(30):
        try:
            client.admin.command("ping")
            print(f"[INFO] MongoDB is responsive. Attempt {attempt + 1}/30")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/30)...")
            time.sleep(2)

    # Initialize replica set
    try:
        client.admin.command("replSetInitiate")
        print("[INFO] MongoDB replica set initiated.")
    except OperationFailure as e:
        print(f"[WARNING] Replica set already initiated: {e}")

    # Wait for PRIMARY node
    for attempt in range(30):
        try:
            status = client.admin.command("replSetGetStatus")
            if status["myState"] == 1:  # PRIMARY node is elected
                print("[INFO] MongoDB PRIMARY node is active.")
                break
        except OperationFailure:
            print(f"[WARNING] Waiting for MongoDB PRIMARY election ({attempt + 1}/30)...")
            time.sleep(2)

    yield mongo.get_connection_url()
    mongo.stop()


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()


@pytest.fixture(scope="module")
def transactions_collection(mongodb_client):
    """Set up the 'transactions' collection in the MongoDB database."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("transactions")
    collection.delete_many({})  # Ensure collection is empty before starting tests
    yield collection
    collection.delete_many({})  # Clean up after tests


def wait_for_primary(mongodb_client):
    """Wait for MongoDB to have an active PRIMARY node before transactions can be executed."""
    print("[INFO] Ensuring MongoDB PRIMARY node is available...")
    for attempt in range(20):
        try:
            status = mongodb_client.admin.command("replSetGetStatus")
            if status["myState"] == 1:  # PRIMARY node must be active
                print("[INFO] MongoDB PRIMARY node is active.")
                return
        except OperationFailure:
            print(f"[WARNING] Waiting for MongoDB PRIMARY election ({attempt + 1}/20)...")
            time.sleep(2)

    raise RuntimeError("MongoDB PRIMARY node did not become available.")
