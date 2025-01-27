import pytest
import pymongo
from testcontainers.mongodb import MongoDbContainer

@pytest.fixture(scope="session")
def mongodb_container():
    """Start a MongoDB container for the entire test session."""
    container = MongoDbContainer("mongo:latest")
    container.start()
    yield container
    container.stop()

@pytest.fixture(scope="function")
def mongodb_client(mongodb_container):
    """Provide a MongoDB client connected to the running Testcontainer."""
    mongo_uri = mongodb_container.get_connection_url()
    client = pymongo.MongoClient(mongo_uri)
    yield client
    client.close()

@pytest.fixture(scope="function")
def mongodb_test_db(mongodb_client):
    """Provide a test database (ensuring isolation between tests)."""
    db = mongodb_client.test_db
    db.drop_collection("data_integrity_test")  # Clean up before each test
    return db
