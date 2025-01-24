import time
import pytest
from pymongo import MongoClient
from testcontainers.core.container import DockerContainer

@pytest.fixture(scope="session")
def mongodb_container():
    """
    Starts a MongoDB container with a properly configured replica set.
    Ensures MongoDB is ready before running tests.
    """
    mongo = (
        DockerContainer("mongo:6.0")
        .with_exposed_ports(27017)  # 🔥 Forces MongoDB to always use a static port
        .with_volume_mapping("/tmp/mongo-data", "/data/db", mode="rw")  # 🔥 Ensures MongoDB has write access
        .with_command("--replSet rs0 --bind_ip_all --setParameter enableTestCommands=1")  # 🔥 Ensures MongoDB properly initializes replica set
    )

    mongo.start()

    connection_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"⏳ Waiting for MongoDB to be ready at {connection_url}")

    # 🔥 Fix: Ensure MongoDB is fully ready before running tests
    client = wait_for_mongo(connection_url)

    # 🔥 Fix: Initialize the replica set properly
    initialize_replica_set(client)

    yield connection_url

    mongo.stop()  # 🔥 Fix: Ensures the container stops properly after tests

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
            client.admin.command("ping")  # 🔥 Ensures MongoDB is responsive before proceeding
            print("✅ MongoDB is ready!")
            return client
        except Exception as e:
            print(f"⏳ MongoDB not ready, retrying ({i}/{retries})... {e}")
            time.sleep(delay)
    raise Exception("🚨 MongoDB failed to start!")

def initialize_replica_set(client, retries=20, delay=3):
    """
    Initializes the MongoDB replica set properly and ensures PRIMARY election completes.
    """
    try:
        print("🔄 Checking if MongoDB Replica Set is already initialized...")
        status = client.admin.command("replSetGetStatus")
        if status.get("myState", 0) == 1:  # 1 = PRIMARY
            print("✅ MongoDB is already PRIMARY!")
            return
    except Exception:
        pass  # Replica set not initialized yet

    print("🔄 Initializing MongoDB Replica Set...")
    client.admin.command("replSetInitiate")

    print("⏳ Waiting for MongoDB to become PRIMARY...")
    for i in range(retries):
        try:
            status = client.admin.command("replSetGetStatus")
            primary = next(
                (m for m in status.get("members", []) if m["stateStr"] == "PRIMARY"),
                None,
            )
            if primary:
                print(f"✅ MongoDB is now PRIMARY ({primary['name']})!")
                return
        except Exception as e:
            print(f"⏳ MongoDB still not PRIMARY, retrying ({i}/{retries})... {e}")
        time.sleep(delay)

    raise Exception("🚨 MongoDB never became PRIMARY, something is wrong!")
