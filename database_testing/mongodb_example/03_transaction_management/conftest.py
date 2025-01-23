import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_client():
    """Start a MongoDB container with a properly configured replica set."""

    print("[INFO] 🚀 Starting MongoDB container...")

    mongo = MongoDbContainer("my-mongo-replica:latest").with_command(
        "--replSet rs0 --bind_ip_all --port 27017"
    )

    mongo.start()

    # ✅ Get MongoDB connection URL
    mongo_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"[INFO] ✅ MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    wait_for_mongo_ready(client)
    wait_for_primary(client)

    yield client  # ✅ Yield the actual client, not just the URL

    print("[INFO] ⏹️ Stopping MongoDB container...")
    mongo.stop()


@pytest.fixture(scope="module")
def transactions_collection(mongodb_client):
    """Provide a MongoDB collection for transaction tests."""
    return mongodb_client.get_database("test_db").get_collection("transactions")
