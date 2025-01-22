import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly configured replica set."""
    
    # Start MongoDB with explicit replica set configuration
    mongo = MongoDbContainer("mongo:6.0").with_command(
        "--replSet rs0 --bind_ip_all --port 27017"
    )
    mongo.start()

    # Get MongoDB connection URL
    mongo_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"[INFO] MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    # Ensure MongoDB starts properly
    wait_for_mongo_ready(client)

    # Ensure MongoDB Replica Set is initialized
    initialize_replica_set(client)

    yield mongo_url  # Yield the correct MongoDB URL
    mongo.stop()


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Return a MongoDB client connected to the Testcontainers MongoDB instance."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()


def wait_for_mongo_ready(client):
    """Wait until MongoDB is ready to accept connections."""
    print("[INFO] Waiting for MongoDB to become responsive...")
    for attempt in range(60):
        try:
            client.admin.command("ping")
            print(f"[INFO] MongoDB is responsive (Attempt {attempt + 1}/60).")
            return
        except ServerSelectionTimeoutError:
            print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/60)...")
            time.sleep(2)
    raise RuntimeError("[ERROR] MongoDB did not become responsive in time.")


def initialize_replica_set(client):
    """Ensure MongoDB replica set is initialized and PRIMARY node is elected."""
    print("[INFO] Initiating MongoDB replica set...")
    
    try:
        client.admin.command("replSetInitiate")
        print("[INFO] MongoDB replica set initiated successfully.")
    except OperationFailure as e:
        if "already initiated" in str(e):
            print("[INFO] MongoDB replica set already initiated.")
        else:
            raise RuntimeError(f"[ERROR] MongoDB replica set initiation failed: {e}")

    # Wait for PRIMARY node election
    print("[INFO] Waiting for MongoDB PRIMARY node election...")
    for attempt in range(60):
        try:
            status = client.admin.command("replSetGetStatus")
            primary_node = next(
                (member for member in status["members"] if member["stateStr"] == "PRIMARY"),
                None
            )

            if primary_node:
                print(f"[INFO] MongoDB PRIMARY node is active: {primary_node['name']}")
                return
        except OperationFailure:
            print(f"[WARNING] Waiting for PRIMARY election ({attempt + 1}/60)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] MongoDB PRIMARY node was not elected.")
