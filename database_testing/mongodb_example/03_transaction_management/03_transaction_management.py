"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""
import pytest
import pymongo

@pytest.mark.transaction
def test_transaction_commit(mongodb_client):
    """Tests MongoDB transaction commit and rollback."""
    
    db = mongodb_client["test_db"]
    users = db["users"]

    session = mongodb_client.start_session()
    session.start_transaction()

    try:
        users.insert_one({"name": "Alice", "email": "alice@example.com"}, session=session)
        users.insert_one({"name": "Bob", "email": "bob@example.com"}, session=session)
        users.update_one({"name": "Alice"}, {"$set": {"email": "alice@updated.com"}}, session=session)

        session.commit_transaction()
        print("[INFO] ✅ Transaction committed successfully.")
    except Exception as e:
        session.abort_transaction()
        print(f"[ERROR] ❌ Transaction failed: {e}")

    session.end_session()

    # Assertions
    assert users.find_one({"name": "Alice"})["email"] == "alice@updated.com"
    assert users.find_one({"name": "Bob"}) is not None
    print("[INFO] ✅ Assertions passed!")

