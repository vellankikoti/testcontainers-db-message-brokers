import pytest 
import time
from pymongo import MongoClient, errors

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
    start_mongo()

    # Get MongoDB URL from Docker Compose setup
    mongo_url = "mongodb://localhost:27017"
    
    # Wait until MongoDB is ready
    wait_for_mongo(mongo_url)

    client = MongoClient(mongo_url)
    yield client
