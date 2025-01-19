import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def source_mongo():
    """Start a MongoDB container for source database."""
    with MongoDbContainer("mongo:6.0") as container:
        connection_url = container.get_connection_url()
        logger.info(f"Source MongoDB container started at {connection_url}")
        yield connection_url

@pytest.fixture(scope="module")
def target_mongo():
    """Start a MongoDB container for target database."""
    with MongoDbContainer("mongo:6.0") as container:
        connection_url = container.get_connection_url()
        logger.info(f"Target MongoDB container started at {connection_url}")
        yield connection_url

@pytest.fixture(scope="module")
def source_client(source_mongo):
    """Create a MongoDB client for source database."""
    client = MongoClient(source_mongo)
    yield client
    client.close()

@pytest.fixture(scope="module")
def target_client(target_mongo):
    """Create a MongoDB client for target database."""
    client = MongoClient(target_mongo)
    yield client
    client.close()
