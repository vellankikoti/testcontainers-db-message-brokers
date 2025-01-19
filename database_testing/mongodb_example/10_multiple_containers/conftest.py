# conftest.py
import pytest
from pymongo import MongoClient
from redis import Redis

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()

@pytest.fixture(scope="module")
def redis_client(redis_container):
    """Create a Redis client connected to the container."""
    client = Redis.from_url(redis_container)
    yield client
    client.close()
