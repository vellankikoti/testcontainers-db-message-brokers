import time
import pytest
from pymongo import MongoClient

MONGO_URI = "mongodb://mongo-db:27017"


def wait_for_primary():
    """Wait for MongoDB to elect a PRIMARY node before running tests."""
    client = MongoClient(MONGO_URI, directConnection=True)
    retries = 30
    while retries > 0:
        try:
            status = client.admin.command("replSetGetStatus")
            primary = any(member["stateStr"] == "PRIMARY" for member in status["members"])
            if primary:
                print("✅ MongoDB PRIMARY node is ready.")
                return
        except Exception as e:
            print(f"🚨 MongoDB not ready, retrying ({30 - retries}/30)... {e}")
        time.sleep(2)
        retries -= 1
    raise Exception("❌ MongoDB PRIMARY node did not start in time.")


@pytest.fixture(scope="session")
def mongodb_client():
    """Ensure MongoDB is running and initialized before tests."""
    wait_for_primary()
    client = MongoClient(MONGO_URI)
    return client
