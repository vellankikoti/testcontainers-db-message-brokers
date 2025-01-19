import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def mongo_container():
    """Start a MongoDB container and provide the connection URL."""
    with MongoDbContainer("mongo:6.0") as container:
        connection_url = container.get_connection_url()
        logger.info(f"MongoDB container started at {connection_url}")
        yield connection_url

@pytest.fixture(scope="module")
def mongo_client(mongo_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongo_container)
    yield client
    client.close()
