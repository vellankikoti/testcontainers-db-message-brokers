import pytest
import time
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
        try:
            container.stop()
            container.wait()  # ✅ Wait for the container to fully stop
            container.remove()
            print(f"[INFO] ✅ Container {container.id} stopped and removed.")
        except docker.errors.APIError as e:
            print(f"[WARNING] ⚠️ Error while stopping/removing {container.id}: {e}")
            time.sleep(2)  # Wait and retry
            try:
                container.remove(force=True)
                print(f"[INFO] ✅ Container {container.id} force removed.")
            except Exception as err:
                print(f"[ERROR] ❌ Could not remove {container.id}: {err}")


@pytest.fixture(scope="module")
def mongodb_client():
    """Start a MongoDB container with a properly configured replica set."""

    stop_existing_mongo_containers()

    print("[INFO] 🚀 Starting MongoDB container...")

    mongo = MongoDbContainer("my-mongo-replica:latest")

    mongo.start()

    mongo_host = "localhost"
    mongo_port = mongo.get_exposed_port(27017)
    mongo_url = f"mongodb://{mongo_host}:{mongo_port}"

    print(f"[INFO] ✅ MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    # ✅ Ensure MongoDB starts properly before proceeding
    wait_for_mongo_ready(client)
    wait_for_primary(client)

    yield client  

    print("[INFO] ⏹️ Stopping MongoDB container...")
    mongo.stop()


def wait_for_mongo_ready(client):
    """Wait until MongoDB is ready before running tests."""
    print("[INFO] ⏳ Waiting for MongoDB to become responsive...")
    for attempt in range(60):  # Increased wait time to 120 seconds
        try:
            client.admin.command("ping")
            print(f"[INFO] ✅ MongoDB is responsive (Attempt {attempt + 1}/60).")
            return
        except ServerSelectionTimeoutError:
            print(f"[WARNING] 🚨 MongoDB not ready, retrying ({attempt + 1}/60)...")
            time.sleep(2)
    raise RuntimeError("[ERROR] ❌ MongoDB did not become responsive in time.")


def wait_for_primary(client):
    """Ensure MongoDB PRIMARY node is elected before running transactions."""
    print("[INFO] ⏳ Waiting for MongoDB PRIMARY node election...")

    for attempt in range(60):  # Increased wait time to 120 seconds
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
            print(f"[WARNING] 🚨 PRIMARY node not available yet, retrying ({attempt + 1}/60)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] ❌ No PRIMARY node found for MongoDB replica set.")
