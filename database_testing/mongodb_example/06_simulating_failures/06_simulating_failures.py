"""
06_simulating_failures.py - Simulating Database Failures

This module demonstrates testing the system's resilience to database failures using MongoDB.
It includes tests for handling connection issues, query execution errors, and transaction rollbacks.
"""

import time
import pytest
from pymongo import MongoClient, errors
from pymongo.write_concern import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.errors import ServerSelectionTimeoutError

# Test data
SAMPLE_ACCOUNTS = [
    {"account_id": "A001", "name": "Alice", "balance": 1000.0},
    {"account_id": "A002", "name": "Bob", "balance": 500.0},
]


@pytest.fixture(scope="module")
def mongodb_client():
    """Create a MongoDB client connected to the replica set."""
    connection_url = "mongodb://localhost:27017/?replicaSet=rs0"
    client = MongoClient(connection_url, serverSelectionTimeoutMS=5000)

    # Wait for the primary to become available
    for attempt in range(10):  # Retry up to 10 times
        try:
            client.admin.command("ping")  # Check if the server is reachable
            status = client.admin.command("replSetGetStatus")
            if any(member["stateStr"] == "PRIMARY" for member in status["members"]):
                print("Replica set primary is ready.")
                break
        except ServerSelectionTimeoutError as e:
            print(f"Attempt {attempt + 1}: Waiting for primary... ({e})")
            time.sleep(2)
    else:
        raise RuntimeError("No primary available in the replica set.")

    yield client
    client.close()


@pytest.fixture(scope="function")
def accounts_db(mongodb_client):
    """Set up the accounts database with sample data."""
    db = mongodb_client.get_database("bank_db")

    # Clean up any existing data
    db.accounts.delete_many({})

    # Set up accounts collection
    accounts_collection = db.get_collection("accounts")
    accounts_collection.insert_many(SAMPLE_ACCOUNTS)

    yield db

    # Cleanup after each test
    db.accounts.delete_many({})


def transfer_funds(db, from_account: str, to_account: str, amount: float) -> bool:
    """Transfer funds between accounts with transaction handling."""
    session = db.client.start_session()
    try:
        with session.start_transaction(
            write_concern=WriteConcern("majority"),
            read_concern=ReadConcern("snapshot"),
            read_preference=ReadPreference.PRIMARY
        ):
            # Deduct from sender's account
            result = db.accounts.update_one(
                {"account_id": from_account, "balance": {"$gte": amount}},
                {"$inc": {"balance": -amount}},
                session=session
            )
            if result.modified_count == 0:
                raise ValueError("Insufficient funds or account not found")

            # Add to recipient's account
            result = db.accounts.update_one(
                {"account_id": to_account},
                {"$inc": {"balance": amount}},
                session=session
            )
            if result.modified_count == 0:
                raise ValueError("Recipient account not found")

            session.commit_transaction()
            return True
    except Exception as e:
        print(f"Transaction failed: {e}")
        if session.in_transaction:
            session.abort_transaction()
        return False
    finally:
        session.end_session()


def test_successful_transfer(accounts_db):
    """Test a successful fund transfer."""
    success = transfer_funds(accounts_db, "A001", "A002", 200.0)
    assert success is True

    # Verify balances
    alice = accounts_db.accounts.find_one({"account_id": "A001"})
    bob = accounts_db.accounts.find_one({"account_id": "A002"})
    assert alice["balance"] == 800.0  # 1000 - 200
    assert bob["balance"] == 700.0    # 500 + 200


def test_insufficient_funds(accounts_db):
    """Test transfer failure due to insufficient funds."""
    success = transfer_funds(accounts_db, "A002", "A001", 600.0)
    assert success is False

    # Verify balances remain unchanged
    alice = accounts_db.accounts.find_one({"account_id": "A001"})
    bob = accounts_db.accounts.find_one({"account_id": "A002"})
    assert alice["balance"] == 1000.0
    assert bob["balance"] == 500.0


def test_recipient_not_found(accounts_db):
    """Test transfer failure due to recipient account not found."""
    success = transfer_funds(accounts_db, "A001", "INVALID", 100.0)
    assert success is False

    # Verify sender's balance remains unchanged
    alice = accounts_db.accounts.find_one({"account_id": "A001"})
    assert alice["balance"] == 1000.0


if __name__ == "__main__":
    """
    Run the tests when the script is executed directly.
    Use -v for verbose output and -s to show print statements.
    """
    import sys
    pytest.main([__file__, "-v", "-s"])
