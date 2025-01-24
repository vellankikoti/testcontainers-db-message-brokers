import pytest
import time
import subprocess
from pymongo import MongoClient, errors

COMPOSE_FILE = "docker-compose.yml"
MONGO_URI = "mongodb://mongo-debug:27017/?replicaSet=rs0"

def start_mongo():
    """Start MongoDB using Docker Compose."""
    print("[INFO] 🚀 Starting MongoDB using Docker Compose...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)

def stop_existing_mongo():
    """Stop and remove any existing MongoDB containers before running tests."""
    print("[INFO] 🛑 Stopping existing MongoDB containers...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "down", "-v"], check=False)

def wait_for_primary(mongo_url, retries=30, delay=2):
    """Ensure MongoDB PRIMARY node is elected before running transactions."""
    print("[INFO] ⏳ Waiting for MongoDB PRIMARY node election...")
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=2000)

    for attempt in range(retries):
        try:
            status = client.admin.command("hello")
            if status.get("isWritablePrimary"):
                print(f"[INFO] 🎉 PRIMARY node elected: {status}")
                return
        except errors.OperationFailure:
            print(f"[WARNING] 🚨 PRIMARY node not available yet, retrying ({attempt+1}/{retries})...")
            time.sleep(delay)

    raise RuntimeError("[ERROR] ❌ No PRIMARY node found for MongoDB replica set.")

@pytest.fixture(scope="session")
def mongodb_client():
    """Ensure MongoDB is running via Docker Compose before tests."""
    
    stop_existing_mongo()
    start_mongo()

    # Ensure MongoDB is fully initialized before running tests
    wait_for_primary(MONGO_URI)

    client = MongoClient(MONGO_URI)
    yield client

    stop_existing_mongo()
