import pytest
import time
import os
import docker
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure


def stop_existing_mongo_containers():
    """Stop and remove any existing MongoDB containers before starting new ones."""
    client = docker.from_env()
    containers = client.containers.list(all=True, filters={"ancestor": "my-mongo-replica"})
    
    for container in containers:
        print(f"[INFO] 🛑 Stopping existing MongoDB container {container.id}...")
        container.stop()
        container.remove()


@pytest.fixture(scope="module")
def mongodb_client():
    """Start a MongoDB container with a properly configured replica set."""

    # ✅ Ensure no MongoDB container is running before starting a new one
    stop_existing_mongo_containers()

    print("[INFO] 🚀 Starting MongoDB container...")

    mongo = MongoDbContainer("my-mongo-replica:latest")

    mongo.start()

    # ✅ Get MongoDB connection URL with correct exposed port
    mongo_host = "localhost"
    mongo_port = mongo.get_exposed_port(27017)
    mongo_url = f"mongodb://{mongo_host}:{mongo_port}"

    print(f"[INFO] ✅ MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    # ✅ Ensure MongoDB starts properly before proceeding
    wait_for_mongo_ready(client)
    wait_for_primary(client)

    yield client  # ✅ Yield the actual MongoDB client

    print("[INFO] ⏹️ Stopping MongoDB container...")
    mongo.stop()


def wait_for_mongo_ready(client):
    """✅ Ensure MongoDB is ready before running tests."""
    print("[INFO] ⏳ Waiting for MongoDB to become responsive...")
    for attempt in range(30):
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

    for attempt in range(30):
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
