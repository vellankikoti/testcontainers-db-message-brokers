import time
import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

@pytest.fixture(scope="session")
def mongodb_container():
    """
    Starts a MongoDB Testcontainers instance with a replica set.
    Ensures MongoDB is ready before running tests.
    """
    with MongoDbContainer("mongo:6.0") as mongo:
        mongo.with_exposed_ports(27017)  # Ensure the correct port is exposed
        mongo.with_command("--replSet rs0")  # Enable replica set mode
        mongo.start()

        connection_url = mongo.get_connection_url()
        print(f"⏳ Waiting for MongoDB to be ready at {connection_url}")

        # Wait for MongoDB to start
        wait_for_mongo(connection_url)

        # Initialize Replica Set
        client = MongoClient(connection_url)
        if not is_replica_set_initialized(client):
            print("🔄 Initializing MongoDB Replica Set...")
            client.admin.command("replSetInitiate")
            time.sleep(5)  # Allow time for initialization
            print("✅ MongoDB Replica Set initialized successfully!")

        yield connection_url

@pytest.fixture(scope="session")
def mongodb_client(mongodb_container):
    """
    Returns a MongoDB client connected to the Testcontainers MongoDB instance.
    """
    client = MongoClient(mongodb_container)
    return client

def wait_for_mongo(uri, retries=30, delay=2):
    """
    Waits for MongoDB to be ready before running tests.
    Retries the connection until MongoDB responds.
    """
    for i in range(retries):
        try:
            client = MongoClient(uri)
            client.admin.command("ping")  # Check if MongoDB is responsive
            print("✅ MongoDB is ready!")
            return client
        except Exception as e:
            print(f"⏳ MongoDB not ready, retrying ({i}/{retries})... {e}")
            time.sleep(delay)
    raise Exception("🚨 MongoDB failed to start!")

def is_replica_set_initialized(client):
    """
    Checks if the MongoDB replica set is already initialized.
    """
    try:
        status = client.admin.command("replSetGetStatus")
        return "set" in status
    except Exception:
        return False
