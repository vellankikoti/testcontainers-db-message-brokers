# conftest.py
import pytest
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()
