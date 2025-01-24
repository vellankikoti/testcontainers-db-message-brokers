import pytest
import time
import subprocess
from pymongo import MongoClient, errors

COMPOSE_FILE = "docker-compose.yml"  # Ensure this file exists in the correct directory

def start_mongo():
    """Start MongoDB using Docker Compose."""
    print("[INFO] 🚀 Starting MongoDB using Docker Compose...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)

def stop_existing_mongo():
    """Stop and remove any existing MongoDB containers before running tests."""
    print("[INFO] 🛑 Stopping existing MongoDB containers...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "down", "-v"], check=False)

def wait_for_mongo(mongo_url, retries=30, delay=2):
    """Wait for MongoDB to become responsive."""
    print("[INFO] ⏳ Waiting for MongoDB to be ready...")
    for attempt in range(retries):
        try:
            client = MongoClient(mongo_url, serverSelectionTimeoutMS=2000)
            client.admin.command("ping")
            print(f"[INFO] ✅ MongoDB is ready (Attempt {attempt+1}/{retries})")
            return True
        except errors.ServerSelectionTimeoutError:
            print(f"[WARNING] 🚨 MongoDB not ready, retrying ({attempt+1}/{retries})...")
            time.sleep(delay)
    raise RuntimeError("[ERROR] ❌ MongoDB did not become responsive in time.")

@pytest.fixture(scope="session")
def mongodb_client():
    """Ensure MongoDB is running via Docker Compose before tests."""
    
    stop_existing_mongo()  # Stop any existing containers
    start_mongo()  # Start MongoDB

    # Get MongoDB URL from Docker Compose setup
    mongo_url = "mongodb://localhost:27017"
    
    # Wait until MongoDB is ready
    wait_for_mongo(mongo_url)

    client = MongoClient(mongo_url)
    yield client

    # Stop containers after tests
    stop_existing_mongo()
