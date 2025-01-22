"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""

import pytest
from pymongo.errors import OperationFailure


def test_transaction_commit(mongodb_client):
    """Test a successful transaction commit."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("transactions")

    # Ensure collection is empty before starting test
    collection.delete_many({})

    with mongodb_client.start_session() as session:
        with session.start_transaction():
            collection.insert_one({"name": "Alice", "balance": 100}, session=session)
            collection.insert_one({"name": "Bob", "balance": 50}, session=session)

        # Commit the transaction
        session.commit_transaction()

    # Verify that the documents are committed successfully
    assert collection.count_documents({"name": "Alice"}) == 1
    assert collection.count_documents({"name": "Bob"}) == 1


def test_transaction_rollback(mongodb_client):
    """Test a transaction rollback scenario."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("transactions")

    # Ensure collection is empty before starting test
    collection.delete_many({})

    with mongodb_client.start_session() as session:
        with pytest.raises(OperationFailure, match="Simulating a failure"):
            with session.start_transaction():
                collection.insert_one({"name": "Charlie", "balance": 200}, session=session)
                
                # Simulate failure before commit
                raise OperationFailure("Simulating a failure")

        # Since the transaction failed, it should have rolled back automatically

    # Verify that no document was inserted due to rollback
    assert collection.count_documents({"name": "Charlie"}) == 0
