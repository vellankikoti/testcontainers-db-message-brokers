import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomMongoContainer(MongoDbContainer):
    """Custom MongoDB container with specific configuration."""

    def __init__(self):
        super().__init__("custom-mongodb:1.0")  # Use the custom MongoDB 1.0 image
        self.with_exposed_ports(27017)

@pytest.fixture(scope="module")
def mongo_container():
    """Fixture to manage MongoDB container lifecycle."""
    logger.info("Starting MongoDB container...")

    with CustomMongoContainer() as container:
        connection_url = container.get_connection_url()  # Get the connection URL
        logger.info(f"MongoDB container started. Connection URL: {connection_url}")
        yield connection_url

@pytest.fixture(scope="module")
def mongo_client(mongo_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongo_container)

    # Wait for MongoDB to be ready
    for _ in range(30):  # Wait up to 30 seconds
        try:
            client.admin.command('ping')  # Check if MongoDB is ready
            logger.info("MongoDB is ready.")
            break
        except Exception:
            logger.warning("Waiting for MongoDB to be ready...")
            time.sleep(1)
    else:
        raise Exception("MongoDB did not start in time.")

    yield client
    client.close()

@pytest.fixture(scope="module")
def accounts_db(mongo_client):
    """Set up the accounts database with sample data."""
    db = mongo_client.get_database("bank_db")  # Use the correct database name

    # Clean up any existing data
    db.accounts.delete_many({})

    # Set up accounts collection
    accounts_collection = db.get_collection("accounts")
    sample_accounts = [
        {"account_id": "A001", "name": "Alice", "balance": 1000.0},
        {"account_id": "A002", "name": "Bob", "balance": 500.0},
    ]

    logger.info("Inserting sample accounts...")
    accounts_collection.insert_many(sample_accounts)

    yield db

    # Cleanup after tests
    logger.info("Cleaning up test data...")
    db.accounts.delete_many({})

def test_account_creation(accounts_db):
    """Test account creation."""
    logger.info("Running test_account_creation")

    # Create new account
    new_account = {
        "account_id": "A003",
        "name": "Charlie",
        "balance": 300.0
    }
    accounts_db.accounts.insert_one(new_account)

    # Verify the account was added
    saved_account = accounts_db.accounts.find_one({"account_id": "A003"})
    assert saved_account is not None
    assert saved_account["name"] == "Charlie"
    assert saved_account["balance"] == 300.0

    logger.info("Account creation test passed")

def test_account_balance_update(accounts_db):
    """Test updating an account's balance."""
    logger.info("Running test_account_balance_update")

    # Update balance
    accounts_db.accounts.update_one(
        {"account_id": "A001"},
        {"$inc": {"balance": 200.0}}
    )

    # Verify the balance was updated
    updated_account = accounts_db.accounts.find_one({"account_id": "A001"})
    assert updated_account["balance"] == 1200.0  # 1000 + 200

    logger.info("Account balance update test passed")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
