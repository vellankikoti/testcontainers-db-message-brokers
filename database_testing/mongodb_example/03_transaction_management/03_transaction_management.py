"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""
import time
import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

@pytest.fixture(scope="module")
def mongodb_container():
    """
    Starts a MongoDB container with a replica set enabled for transactions.
    """
    with MongoDbContainer("mongo:6.0") as mongo:
        mongo.with_command("--replSet rs0")  # Enable replica set mode
        mongo.start()

        # Wait for MongoDB to fully start
        time.sleep(5)

        # Initialize the replica set
        client = MongoClient(mongo.get_connection_url())
        client.admin.command("replSetInitiate")
        time.sleep(5)  # Allow time for initialization

        yield mongo.get_connection_url()

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """
    Returns a MongoDB client connected to the Testcontainers MongoDB instance.
    """
    client = MongoClient(mongodb_container)
    return client

def test_transaction_commit(mongodb_client):
    """
    Tests MongoDB transactions by committing and rolling back operations.
    """
    db = mongodb_client["test_db"]
    users_collection = db["users"]
    session = mongodb_client.start_session()

    try:
        # Begin Transaction
        session.start_transaction()

        # Insert Documents
        users_collection.insert_one({"name": "Alice", "email": "alice@example.com"}, session=session)
        users_collection.insert_one({"name": "Bob", "email": "bob@example.com"}, session=session)

        # Update Document
        users_collection.update_one({"name": "Alice"}, {"$set": {"email": "alice@updated.com"}}, session=session)

        # Commit Transaction
        session.commit_transaction()

        # Validate that the changes persisted
        assert users_collection.find_one({"name": "Alice"})["email"] == "alice@updated.com"
        assert users_collection.find_one({"name": "Bob"}) is not None

    finally:
        session.end_session()

def test_transaction_rollback(mongodb_client):
    """
    Tests that rollback properly undoes all operations within a transaction.
    """
    db = mongodb_client["test_db"]
    users_collection = db["users"]
    session = mongodb_client.start_session()

    try:
        # Begin Transaction
        session.start_transaction()

        # Insert Document
        users_collection.insert_one({"name": "Charlie", "email": "charlie@example.com"}, session=session)

        # Rollback Transaction
        session.abort_transaction()

        # Validate that Charlie does not exist
        assert users_collection.find_one({"name": "Charlie"}) is None

    finally:
        session.end_session()

