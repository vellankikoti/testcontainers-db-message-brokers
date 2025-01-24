import pytest
import time
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

@pytest.fixture(scope="session")
def mongodb_container():
    """
    Starts a MongoDB container with a Replica Set (required for transactions).
    Ensures MongoDB stays running by keeping a writable volume.
    """
    with MongoDbContainer("mongo:6.0") \
        .with_exposed_ports(27017) \
        .with_env("MONGO_INITDB_ROOT_USERNAME", "test") \
        .with_env("MONGO_INITDB_ROOT_PASSWORD", "test") \
        .with_env("MONGO_INITDB_DATABASE", "test_db") \
        .with_command("--replSet rs0 --bind_ip_all") \
        .with_volume_mapping("/tmp/mongo-data", "/data/db", mode="rw") as mongo:

        mongo_url = f"mongodb://test:test@localhost:{mongo.get_exposed_port(27017)}/test_db"

        print(f"⏳ Waiting for MongoDB to be ready at {mongo_url}")
        wait_for_mongo(mongo_url)

        print("🔄 Initializing MongoDB Replica Set...")
        initialize_replica_set(mongo_url)

        yield mongo_url

@pytest.fixture(scope="function")
def mongodb_client(mongodb_container):
    """Provides a MongoDB client for tests."""
    client = MongoClient(mongodb_container)
    db = client["test_db"]
    yield db
    client.close()

def wait_for_mongo(mongo_url):
    """Retries MongoDB connection until it's ready."""
    client = MongoClient(mongo_url)
    for _ in range(30):
        try:
            client.admin.command("ping")
            print("✅ MongoDB is ready!")
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError("❌ MongoDB failed to start!")

def initialize_replica_set(mongo_url):
    """Initializes MongoDB replica set to avoid transaction issues."""
    client = MongoClient(mongo_url)
    try:
        client.admin.command("replSetInitiate", {
            "_id": "rs0",
            "members": [{"_id": 0, "host": "localhost:27017"}]
        })
    except Exception as e:
        print(f"⚠️ Replica set initialization error: {e}")
    
    for _ in range(30):
        status = client.admin.command("replSetGetStatus")
        if status["myState"] == 1:
            print("✅ MongoDB is now PRIMARY!")
            return
        time.sleep(2)
    raise RuntimeError("❌ MongoDB failed to become PRIMARY!")
