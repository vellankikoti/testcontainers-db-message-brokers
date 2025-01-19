# conftest.py
import pytest
from pymongo import MongoClient

@pytest.fixture(scope="module")
def mongodb_client_1(mongodb_container_1):
    """Create a MongoDB client connected to the first container."""
    client = MongoClient(mongodb_container_1)
    yield client
    client.close()

@pytest.fixture(scope="module")
def mongodb_client_2(mongodb_container_2):
    """Create a MongoDB client connected to the second container."""
    client = MongoClient(mongodb_container_2)
    yield client
    client.close()
