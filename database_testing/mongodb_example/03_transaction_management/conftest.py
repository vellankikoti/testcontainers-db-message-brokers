import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly configured replica set."""

    # ✅ Use the custom MongoDB image with replica set initialized
    mongo = MongoDbContainer("my-mongo-replica:latest").with_command(
        "--replSet rs0 --bind_ip_all --port 27017"
    )
    mongo.start()

    # ✅ Get MongoDB connection URL
    mongo_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"[INFO] MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    # ✅ Ensure MongoDB starts properly before proceeding
    wait_for_mongo_ready(client)

    yield mongo_url  # ✅ Yield the correct MongoDB URL to test functions
    mongo.stop()


@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Return a MongoDB client connected to the Testcontainers MongoDB instance."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()


def wait_for_mongo_ready(client):
    """✅ Ensure MongoDB is ready before running tests."""
    print("[INFO] Waiting for MongoDB to become responsive...")
    for attempt in range(30):  # Maximum wait time: 60 seconds
        try:
            client.admin.command("ping")
            print(f"[INFO] MongoDB is responsive (Attempt {attempt + 1}/30).")
            return
        except ServerSelectionTimeoutError:
            print(f"[WARNING] MongoDB not ready, retrying ({attempt + 1}/30)...")
            time.sleep(2)
    raise RuntimeError("[ERROR] MongoDB did not become responsive in time.")
