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
        mongo.with_exposed_ports(27017)  # Explicitly expose port to avoid conflicts
        mongo.with_command("--replSet rs0")  # Enable replica set
        mongo.start()
        
        connection_url = mongo.get_connection_url()
        print(f"⏳ Waiting for MongoDB to be ready at {connection_url}")

        # Wait for MongoDB to be accessible
        wait_for_mongo(connection_url)

        # Initialize Replica Set
        client = MongoClient(connection_url)
        try:
            client.admin.command("replSetInitiate")
            print("✅ MongoDB Replica Set initialized successfully!")
        except Exception as e:
            print(f"⚠️ Replica Set already initialized or failed: {e}")

        time.sleep(5)  # Allow some time for replication setup

        yield connection_url

@pytest.fixture(scope="session")
def mongodb_client(mongodb_container):
    """
    Returns a MongoDB client connected to the Testcontainers MongoDB instance.
    """
    client = MongoClient(mongodb_container)
    return client

def wait_for_mongo(uri, retries=30, delay=3):
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
