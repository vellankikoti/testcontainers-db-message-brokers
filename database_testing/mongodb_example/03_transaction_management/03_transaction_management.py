"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""
import pytest
from pymongo import MongoClient

@pytest.mark.transaction
def test_transaction_commit(mongodb_client):
    """Tests MongoDB transaction commit and rollback."""

    db = mongodb_client["test_db"]
    users_collection = db["users"]

    session = mongodb_client.start_session()  # Explicitly start session
    session.start_transaction()

    # Insert sample data
    users_collection.insert_one({"name": "Alice", "email": "alice@example.com"}, session=session)
    users_collection.insert_one({"name": "Bob", "email": "bob@example.com"}, session=session)

    # Commit the transaction
    session.commit_transaction()

    # Validate committed data
    assert users_collection.find_one({"name": "Alice"})["email"] == "alice@example.com"
    assert users_collection.find_one({"name": "Bob"}) is not None

    # Rollback test
    session.start_transaction()
    users_collection.delete_one({"name": "Alice"}, session=session)
    session.abort_transaction()

    # Ensure rollback worked
    assert users_collection.find_one({"name": "Alice"}) is not None
