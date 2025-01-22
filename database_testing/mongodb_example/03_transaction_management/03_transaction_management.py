"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""

import pytest
from pymongo.errors import OperationFailure
import time


def wait_for_primary(mongodb_client):
    """Wait for MongoDB to have an active PRIMARY node before transactions can be executed."""
    print("[INFO] Waiting for MongoDB PRIMARY node to become available...")
    for attempt in range(20):
        try:
            status = mongodb_client.admin.command("replSetGetStatus")
            if status["myState"] == 1:  # PRIMARY node must be active
                print("[INFO] MongoDB PRIMARY node is active.")
                return
        except OperationFailure:
            print(f"[WARNING] Waiting for MongoDB PRIMARY election ({attempt + 1}/20)...")
            time.sleep(2)
    
    raise RuntimeError("MongoDB PRIMARY node did not become available.")


def test_transaction_commit(mongodb_client, mongo_session, transactions_collection):
    """Test a successful transaction commit."""
    wait_for_primary(mongodb_client)

    with mongo_session.start_transaction():
        transactions_collection.insert_one({"name": "Alice", "balance": 100}, session=mongo_session)
        transactions_collection.insert_one({"name": "Bob", "balance": 50}, session=mongo_session)
        mongo_session.commit_transaction()

    assert transactions_collection.count_documents({"name": "Alice"}) == 1
    assert transactions_collection.count_documents({"name": "Bob"}) == 1


def test_transaction_rollback(mongodb_client, mongo_session, transactions_collection):
    """Test a transaction rollback scenario."""
    wait_for_primary(mongodb_client)

    with pytest.raises(OperationFailure):
        with mongo_session.start_transaction():
            transactions_collection.insert_one({"name": "Charlie", "balance": 200}, session=mongo_session)
            raise OperationFailure("Simulating a failure")
            mongo_session.commit_transaction()

    assert transactions_collection.count_documents({"name": "Charlie"}) == 0
