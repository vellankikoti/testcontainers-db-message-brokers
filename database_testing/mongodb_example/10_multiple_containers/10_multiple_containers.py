"""
10_multiple_containers.py - Testing Interactions Between MongoDB and Redis

This example demonstrates how to use Testcontainers to test interactions between a MongoDB database and a Redis cache.
"""

import pytest
from pymongo import MongoClient
from redis import Redis
from testcontainers.mongodb import MongoDbContainer
from testcontainers.redis import RedisContainer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container."""
    with MongoDbContainer("mongo:6.0") as mongo:
        yield mongo.get_connection_url()

@pytest.fixture(scope="module")
def redis_container():
    """Start a Redis container."""
    with RedisContainer("redis:6.0") as redis:
        yield f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}"

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

def test_mongo_to_redis(mongodb_client, redis_client):
    """Test data migration from MongoDB to Redis."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("customers")

    # Insert sample data into MongoDB
    sample_data = [
        {"customer_id": "C001", "name": "John Doe", "email": "john@example.com"},
        {"customer_id": "C002", "name": "Jane Smith", "email": "jane@example.com"},
    ]
    collection.insert_many(sample_data)
    logger.info("Inserted sample data into MongoDB")

    # Migrate data from MongoDB to Redis
    for customer in collection.find():
        redis_client.set(customer["customer_id"], customer["name"])
        logger.info(f"Migrated customer {customer['customer_id']} to Redis")

    # Verify data in Redis
    for customer in sample_data:
        name = redis_client.get(customer["customer_id"])
        assert name.decode('utf-8') == customer["name"], f"Expected {customer['name']} but got {name.decode('utf-8')}"

def test_redis_operations(redis_client):
    """Test basic Redis operations."""
    redis_client.set("test_key", "test_value")
    value = redis_client.get("test_key")
    assert value.decode('utf-8') == "test_value", f"Expected 'test_value' but got {value.decode('utf-8')}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
