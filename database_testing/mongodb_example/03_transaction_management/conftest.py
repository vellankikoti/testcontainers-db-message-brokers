import pytest
import subprocess
import time
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

COMPOSE_FILE = "docker-compose.yml"

def stop_existing_mongo():
    """Stop any running MongoDB containers using Docker Compose."""
    print("[INFO] 🛑 Stopping existing MongoDB containers...")
    try:
        # Use "docker compose" (without hyphen)
        subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "down", "-v"], check=True)
        print("[INFO] ✅ Existing MongoDB containers stopped.")
    except subprocess.CalledProcessError as e:
        print(f"[WARNING] ⚠️ Error while stopping MongoDB: {e}")


@pytest.fixture(scope="session")
def mongodb_client():
    """Start MongoDB using Docker Compose with a properly initialized replica set."""
    
    # Stop any running MongoDB instance
    stop_existing_mongo()

    print("[INFO] 🚀 Starting MongoDB using Docker Compose...")
    try:
        subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)
        print("[INFO] ✅ MongoDB container started.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"[ERROR] ❌ Failed to start MongoDB container: {e}")

    # Wait for MongoDB to be ready
    mongo_url = "mongodb://localhost:27017"
    client = MongoClient(mongo_url)
    wait_for_mongo_ready(client)
    wait_for_primary(client)

    yield client  # Provide the client to tests

    # Cleanup after tests
    print("[INFO] ⏹️ Stopping MongoDB after tests...")
    stop_existing_mongo()


def wait_for_mongo_ready(client, retries=30, delay=2):
    """Ensure MongoDB is ready before running tests."""
    print("[INFO] ⏳ Waiting for MongoDB to become responsive...")
    for attempt in range(retries):
        try:
            client.admin.command("ping")
            print(f"[INFO] ✅ MongoDB is responsive (Attempt {attempt + 1}/{retries}).")
            return
        except ServerSelectionTimeoutError:
            print(f"[WARNING] 🚨 MongoDB not ready, retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)
    raise RuntimeError("[ERROR] ❌ MongoDB did not become responsive in time.")


def wait_for_primary(client, retries=30, delay=2):
    """Ensure MongoDB PRIMARY node is elected before running transactions."""
    print("[INFO] ⏳ Waiting for MongoDB PRIMARY node election...")
    for attempt in range(retries):
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
            print(f"[WARNING] 🚨 PRIMARY node not available yet, retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)

    raise RuntimeError("[ERROR] ❌ No PRIMARY node found for MongoDB replica set.")
