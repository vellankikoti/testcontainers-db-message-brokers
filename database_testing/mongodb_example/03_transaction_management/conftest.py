import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container with a properly configured replica set."""

    print("[DEBUG] 🔍 Checking if Testcontainers is using the correct MongoDB image...")

    mongo = MongoDbContainer("my-mongo-replica:latest").with_command(
        "--replSet rs0 --bind_ip_all --port 27017"
    )

    print("[INFO] 🚀 Starting MongoDB container...")
    mongo.start()

    # Debugging: Print container logs
    print("[DEBUG] 🔍 MongoDB Container Logs:")
    print(mongo.get_logs())  # Print logs directly

    # Get MongoDB connection URL
    mongo_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"[INFO] ✅ MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    wait_for_mongo_ready(client)
    wait_for_primary(client)

    yield mongo_url  # ✅ Yield the correct MongoDB URL to test functions

    print("[INFO] ⏹️ Stopping MongoDB container...")
    mongo.stop()


def wait_for_mongo_ready(client):
    """✅ Ensure MongoDB is ready before running tests."""
    print("[INFO] ⏳ Waiting for MongoDB to become responsive...")
    for attempt in range(30):  # Maximum wait time: 60 seconds
        try:
            client.admin.command("ping")
            print(f"[INFO] ✅ MongoDB is responsive (Attempt {attempt + 1}/30).")
            return
        except ServerSelectionTimeoutError:
            print(f"[WARNING] 🚨 MongoDB not ready, retrying ({attempt + 1}/30)...")
            time.sleep(2)
    raise RuntimeError("[ERROR] ❌ MongoDB did not become responsive in time.")


def wait_for_primary(client):
    """✅ Ensure MongoDB PRIMARY node is elected before running transactions."""
    print("[INFO] ⏳ Waiting for MongoDB PRIMARY node election...")

    for attempt in range(30):  # Maximum wait time: 60 seconds
        try:
            status = client.admin.command("replSetGetStatus")
            primary_node = next(
                (member for member in status["members"] if member["stateStr"] == "PRIMARY"),
                None
            )
            if primary_node:
                print(f"[INFO] 🎉 PRIMARY node elected: {primary_node['name']}")
                return
        except OperationFailure:
            print(f"[WARNING] 🚨 PRIMARY node not available yet, retrying ({attempt + 1}/30)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] ❌ No PRIMARY node found for MongoDB replica set.")
