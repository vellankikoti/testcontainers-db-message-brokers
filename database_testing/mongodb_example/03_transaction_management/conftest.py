import time
import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

@pytest.fixture(scope="session")
def mongodb_container():
    """
    Starts a MongoDB container with a properly configured replica set.
    Ensures MongoDB is PRIMARY before running tests.
    """
    mongo = MongoDbContainer("mongo:6.0").with_command(
        "--replSet rs0 --bind_ip_all --setParameter enableTestCommands=1"
    )
    mongo.start()

    connection_url = f"mongodb://localhost:{mongo.get_exposed_port(27017)}"
    print(f"⏳ Waiting for MongoDB to be ready at {connection_url}")

    client = wait_for_mongo(connection_url)
    initialize_replica_set(client)  # 🔥 Ensure MongoDB becomes PRIMARY

    yield connection_url
    mongo.stop()

@pytest.fixture(scope="session")
def mongodb_client(mongodb_container):
    return MongoClient(mongodb_container)

def wait_for_mongo(uri, retries=30, delay=2):
    """
    Waits for MongoDB to be ready before running tests.
    """
    for i in range(retries):
        try:
            client = MongoClient(uri)
            client.admin.command("ping")
            print("✅ MongoDB is ready!")
            return client
        except Exception as e:
            print(f"⏳ MongoDB not ready, retrying ({i}/{retries})... {e}")
            time.sleep(delay)
    raise Exception("🚨 MongoDB failed to start!")

def initialize_replica_set(client, retries=30, delay=3):
    """
    Ensures MongoDB becomes PRIMARY by initializing the Replica Set and waiting for election completion.
    """
    try:
        status = client.admin.command("replSetGetStatus")
        if status.get("myState") == 1:  # 1 = PRIMARY
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
