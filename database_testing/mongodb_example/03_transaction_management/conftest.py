import pytest
import time
import docker
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import subprocess

COMPOSE_FILE = "docker-compose.yml"

def stop_existing_mongo():
    """Stop and remove existing MongoDB container using Docker Compose."""
    print("[INFO] 🛑 Stopping MongoDB (docker-compose down)...")
    subprocess.run(["docker compose", "-f", COMPOSE_FILE, "down", "-v"], check=False)

@pytest.fixture(scope="session")
def mongodb_client():
    """Start MongoDB via Docker Compose with proper replica set initialization."""
    
    stop_existing_mongo()

    print("[INFO] 🚀 Starting MongoDB using Docker Compose...")
    subprocess.run(["docker-compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)

    time.sleep(5)  # Wait for MongoDB to start

    mongo_url = "mongodb://localhost:27017"
    print(f"[INFO] ✅ MongoDB connection URL: {mongo_url}")

    client = MongoClient(mongo_url)

    ensure_replica_set(client)

    yield client  # Yield actual MongoDB client

    print("[INFO] ⏹️ Stopping MongoDB container...")
    stop_existing_mongo()


def ensure_replica_set(client):
    """Ensure the replica set is properly initialized."""
    print("[INFO] 🔄 Checking MongoDB replica set status...")
    try:
        status = client.admin.command("replSetGetStatus")
        if status["ok"] == 1:
            print("[INFO] ✅ Replica set is already initialized.")
            return
    except OperationFailure:
        print("[WARNING] 🚨 Replica set not initialized. Initializing now...")

    try:
        client.admin.command("replSetInitiate", {
            "_id": "rs0",
            "members": [{ "_id": 0, "host": "localhost:27017" }]
        })
        print("[INFO] 🎉 Replica set initialized successfully!")
    except OperationFailure as e:
        print(f"[ERROR] ❌ Failed to initialize replica set: {e}")
        raise

    print("[INFO] ⏳ Waiting for MongoDB to elect a PRIMARY node...")
    for attempt in range(60):
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
            print(f"[WARNING] 🚨 PRIMARY node not ready, retrying ({attempt + 1}/60)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] ❌ No PRIMARY node found for MongoDB replica set.")
