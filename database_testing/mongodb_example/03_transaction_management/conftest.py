import pytest
import pymongo
import subprocess
import time

COMPOSE_FILE = "docker-compose.yml"
MONGO_URI = "mongodb://localhost:27017"

def stop_existing_mongo():
    """Stops existing MongoDB containers"""
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "down", "-v"], check=False)

def start_mongo():
    """Starts MongoDB using Docker Compose"""
    subprocess.run(["docker", "compose", "-f", COMPOSE_FILE, "up", "-d"], check=True)
    wait_for_primary()

def wait_for_primary():
    """Waits until MongoDB elects a PRIMARY node"""
    client = pymongo.MongoClient(MONGO_URI)
    for i in range(30):
        try:
            status = client.admin.command("replSetGetStatus")
            primary = any(m["stateStr"] == "PRIMARY" for m in status["members"])
            if primary:
                print("[INFO] ✅ PRIMARY node elected.")
                return
        except Exception:
            pass
        print(f"[WARNING] 🚨 PRIMARY node not available yet, retrying ({i+1}/30)...")
        time.sleep(2)
    raise Exception("[ERROR] ❌ MongoDB PRIMARY node not available!")

@pytest.fixture(scope="session")
def mongodb_client():
    """Ensures MongoDB is running before tests"""
    stop_existing_mongo()
    start_mongo()
    client = pymongo.MongoClient(MONGO_URI)
    yield client
    client.close()
    stop_existing_mongo()
