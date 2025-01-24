import os
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
    mongo = MongoDbContainer("mongo:6.0")
    mongo.with_exposed_ports(27017)  # 🔥 Fix: Forces MongoDB to always run on port 27017
    mongo.with_command("--replSet rs0")  # 🔥 Fix: Ensures transactions are supported
    mongo.start()

    connection_url = f"mongodb://localhost:27017"  # 🔥 Fix: No more dynamic ports
    print(f"⏳ Waiting for MongoDB to be ready at {connection_url}")

    # 🔥 Fix: Ensure MongoDB is fully ready before running tests
    wait_for_mongo(connection_url)

    # 🔥 Fix: Properly initialize the replica set if needed
    client = MongoClient(connection_url)
    if not is_replica_set_initialized(client):
        print("🔄 Initializing MongoDB Replica Set...")
        client.admin.command("replSetInitiate")
        time.sleep(5)  # Allow time for initialization
        print("✅ MongoDB Replica Set initialized successfully!")

    yield connection_url  # 🔥 Fix: Ensures the same container is used across all tests

    mongo.stop()  # 🔥 Fix: Ensure the container stops properly after tests

@pytest.fixture(scope="session")
def mongodb_client(mongodb_container):
    """
    Returns a MongoDB client connected to the Testcontainers MongoDB instance.
    """
    return MongoClient(mongodb_container)

def wait_for_mongo(uri, retries=30, delay=2):
    """
    Waits for MongoDB to be ready before running tests.
    Retries the connection until MongoDB responds.
    """
    for i in range(retries):
        try:
            client = MongoClient(uri)
            client.admin.command("ping")  # 🔥 Fix: Ensures MongoDB is responsive before proceeding
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
