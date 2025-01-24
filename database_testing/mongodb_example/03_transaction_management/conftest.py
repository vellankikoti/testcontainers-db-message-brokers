import pytest
import time
import subprocess
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

COMPOSE_FILE = "docker-compose.yml"

def stop_existing_mongo():
    """Stops and removes any existing MongoDB containers before running tests."""
    print("[INFO] 🛑 Stopping existing MongoDB containers...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "down", "-v"], check=False)
    print("[INFO] ✅ Existing MongoDB containers stopped.")

@pytest.fixture(scope="session")
def mongodb_client():
    """Start MongoDB via Docker Compose with proper replica set initialization."""
    
    stop_existing_mongo()

    print("[INFO] 🚀 Starting MongoDB using Docker Compose...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)
    print("[INFO] ✅ MongoDB container started.")

    # ✅ Wait until MongoDB is ready before proceeding
    mongo_url = "mongodb://localhost:27017"
    client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)

    for attempt in range(30):  # Wait up to 60 seconds
        try:
            client.admin.command("ping")
            print(f"[INFO] ✅ MongoDB is responsive (Attempt {attempt + 1}/30).")
            break
        except ServerSelectionTimeoutError:
            print(f"[WARNING] 🚨 MongoDB not ready, retrying ({attempt + 1}/30)...")
            time.sleep(2)
    else:
        raise RuntimeError("[ERROR] ❌ MongoDB did not become responsive in time.")

    yield client

    print("[INFO] ⏹️ Stopping MongoDB after tests...")
    stop_existing_mongo()
