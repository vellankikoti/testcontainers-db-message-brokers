import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_container():
    """Setup MongoDB Testcontainer."""
    with MongoDbContainer("mongo:6.0") as mongo:
        yield mongo.get_connection_url()
