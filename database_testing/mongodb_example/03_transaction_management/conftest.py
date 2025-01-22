import pytest
import time
import os
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly configured replica set."""
    
    # Define the absolute path to the mongo-init.js script
    init_script_path = os.path.abspath("mongo-init.js")

    # Start MongoDB with replica set and init script
    mongo = MongoDbContainer("mongo:6.0").with_command(
        "--replSet rs0 --bind_ip_all --port 27017"
    ).with_volume_mapping(init_script_path, "/docker-entrypoint-initdb.d/mongo-init.js")

    mongo.start()

    # Get MongoDB connection URL
    mongo_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"[INFO] MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    # Wait for MongoDB to become responsive
    print("[INFO] Waiting for MongoDB to become responsive...")
    for attempt in range(60):  # Wait up to 2 minutes
        try:
            client.admin.command("ping")
            print(f"[INFO] MongoDB is responsive (Attempt {attempt + 1}/60).")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/60)...")
            time.sleep(2)
    else:
        raise RuntimeError("[ERROR] MongoDB did not become responsive in time.")

    # Wait for PRIMARY node election
    print("[INFO] Waiting for MongoDB PRIMARY node election...")
    for attempt in range(60):  # Increased timeout to 2 minutes
        try:
            status = client.admin.command("replSetGetStatus")
            primary_node = None
            for member in status["members"]:
                if member["stateStr"] == "PRIMARY":
                    primary_node = member
                    break

            if primary_node:
                print(f"[INFO] MongoDB PRIMARY node is active: {primary_node['name']}")
                break
        except OperationFailure:
            print(f"[WARNING] Waiting for PRIMARY election ({attempt + 1}/60)...")
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
    for attempt in range(30):
        try:
            status = mongodb_client.admin.command("replSetGetStatus")
            if any(member["stateStr"] == "PRIMARY" for member in status["members"]):
                print("[INFO] MongoDB PRIMARY node is active.")
                return
        except OperationFailure:
            print(f"[WARNING] Waiting for PRIMARY election ({attempt + 1}/30)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] MongoDB PRIMARY node did not become available.")
