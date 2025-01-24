import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
import time

@pytest.fixture(scope="session")
def mongodb_container():
    mongo_container = (
        MongoDbContainer("mongo:6.0")
        .with_exposed_ports(27017)
        .with_command("mongod --replSet rs0 --bind_ip_all --keyFile /tmp/mongo-keyfile")
        .with_volume_mapping("/tmp/mongo-keyfile", "/tmp/mongo-keyfile", mode="rw")  # Mount keyFile
        .with_volume_mapping("/tmp/mongo-data", "/data/db", mode="rw")  # Persistent Data
    )

    with mongo_container as mongo:
        mongo_url = mongo.get_connection_url()
        client = MongoClient(mongo_url)
        
        # Wait for MongoDB to start
        time.sleep(5)

        # Initiate Replica Set
        client.admin.command("replSetInitiate")
        time.sleep(5)  # Give it time to initialize

        yield mongo_url
