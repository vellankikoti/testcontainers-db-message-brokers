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
    session = mongodb_client.start_session()

    with session.start_transaction():
        collection.insert_one({"name": "Alice", "balance": 100}, session=session)
        collection.insert_one({"name": "Bob", "balance": 50}, session=session)
        session.commit_transaction()
    
    assert collection.count_documents({"name": "Alice"}) == 1
    assert collection.count_documents({"name": "Bob"}) == 1


def test_transaction_rollback(mongodb_client):
    """Test a transaction rollback scenario."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("transactions")
    session = mongodb_client.start_session()

    with pytest.raises(OperationFailure):
        with session.start_transaction():
            collection.insert_one({"name": "Charlie", "balance": 200}, session=session)
            raise OperationFailure("Simulating a failure")
            session.commit_transaction()
    
    assert collection.count_documents({"name": "Charlie"}) == 0