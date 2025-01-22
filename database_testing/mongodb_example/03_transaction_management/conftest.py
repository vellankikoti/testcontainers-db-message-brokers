import pytest
import time
import os
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly configured replica set."""
    mongo = MongoDbContainer("mongo:6.0").with_command(
        "--replSet rs0 --bind_ip_all --port 27017"
    )
    mongo.start()

    # Get connection details
    mongo_url = mongo.get_connection_url()
    print(f"[INFO] MongoDB connection URL: {mongo_url}")

    # Create a MongoDB client
    client = MongoClient(mongo_url)

    # Wait for MongoDB to be responsive
    for attempt in range(30):
        try:
            client.admin.command("ping")
            print(f"[INFO] MongoDB is responsive (Attempt {attempt + 1}/30).")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/30)...")
            time.sleep(2)
    else:
        raise RuntimeError("[ERROR] MongoDB did not become responsive in time.")

    # Initialize replica set (Retry if necessary)
    print("[INFO] Initiating MongoDB replica set...")
    for attempt in range(10):
        try:
            client.admin.command("replSetInitiate")
            print("[INFO] MongoDB replica set initiated successfully.")
            break
        except OperationFailure as e:
            if "already initiated" in str(e):
                print("[INFO] MongoDB replica set already initiated.")
                break
            print(f"[WARNING] Failed to initiate replica set, retrying ({attempt + 1}/10)...")
            time.sleep(2)
    else:
        raise RuntimeError("[ERROR] MongoDB replica set did not initialize.")

    # Wait for PRIMARY node election
    print("[INFO] Waiting for MongoDB PRIMARY node election...")
    for attempt in range(30):
        try:
            status = client.admin.command("replSetGetStatus")
            primary = any(member["stateStr"] == "PRIMARY" for member in status["members"])
            if primary:
                print("[INFO] MongoDB PRIMARY node is active.")
                break
        except OperationFailure:
            print(f"[WARNING] Waiting for PRIMARY election ({attempt + 1}/30)...")
            time.sleep(2)
    else:
        raise RuntimeError("[ERROR] MongoDB PRIMARY node was not elected.")

    yield mongo_url  # Yield the correct MongoDB URL
    mongo.stop()


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the Testcontainers MongoDB instance."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()


@pytest.fixture(scope="module")
def transactions_collection(mongodb_client):
    """Set up the 'transactions' collection in the MongoDB database."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("transactions")
    collection.delete_many({})  # Ensure collection is empty before tests
    yield collection
    collection.delete_many({})  # Clean up after tests


def wait_for_primary(mongodb_client):
    """Ensure MongoDB has an active PRIMARY node before running transactions."""
    print("[INFO] Ensuring MongoDB PRIMARY node is available...")
    for attempt in range(20):
        try:
            status = mongodb_client.admin.command("replSetGetStatus")
            if any(member["stateStr"] == "PRIMARY" for member in status["members"]):
                print("[INFO] MongoDB PRIMARY node is active.")
                return
        except OperationFailure:
            print(f"[WARNING] Waiting for PRIMARY election ({attempt + 1}/20)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] MongoDB PRIMARY node did not become available.")
