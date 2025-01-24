import pytest
from pymongo import MongoClient

def test_transaction_commit(mongodb_client):
    """
    Tests MongoDB transactions using Testcontainers.
    Ensures data is committed successfully.
    """
    db = mongodb_client["test_db"]
    collection = db["users"]

    session = mongodb_client.start_session()
    session.start_transaction()

    collection.insert_one({"name": "Alice", "email": "alice@example.com"}, session=session)
    collection.insert_one({"name": "Bob", "email": "bob@example.com"}, session=session)

    session.commit_transaction()
    session.end_session()

    assert collection.find_one({"name": "Alice"})["email"] == "alice@example.com"
    assert collection.find_one({"name": "Bob"}) is not None
    print("✅ Transaction Commit Test Passed!")

def test_transaction_rollback(mongodb_client):
    """
    Tests MongoDB rollback transactions.
    Ensures changes do NOT persist on rollback.
    """
    db = mongodb_client["test_db"]
    collection = db["users"]

    session = mongodb_client.start_session()
    session.start_transaction()

    collection.insert_one({"name": "Charlie", "email": "charlie@example.com"}, session=session)

    session.abort_transaction()
    session.end_session()

    assert collection.find_one({"name": "Charlie"}) is None
    print("✅ Transaction Rollback Test Passed!")
