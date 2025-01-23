"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""
import pytest
from pymongo.errors import OperationFailure


@pytest.fixture(scope="module")
def transactions_collection(mongodb_client):
    """Provide a MongoDB collection for transaction tests."""
    return mongodb_client.get_database("test_db").get_collection("transactions")


def wait_for_primary(client):
    """Ensure a MongoDB PRIMARY node is elected before running transactions."""
    print("[INFO] Waiting for MongoDB PRIMARY node election...")

    for attempt in range(30):  # Maximum wait time: 60 seconds
        try:
            status = client.admin.command("replSetGetStatus")
            primary_node = next(
                (member for member in status["members"] if member["stateStr"] == "PRIMARY"),
                None
            )
            if primary_node:
                print(f"[INFO] PRIMARY node elected: {primary_node['name']}")
                return
        except OperationFailure:
            print(f"[WARNING] PRIMARY node not available yet, retrying ({attempt + 1}/30)...")
            time.sleep(2)

    raise RuntimeError("[ERROR] No PRIMARY node found for MongoDB replica set.")


def test_transaction_commit(mongodb_client, transactions_collection):
    """Test a successful transaction commit."""
    wait_for_primary(mongodb_client)  # Ensure PRIMARY before running transactions

    db = mongodb_client.get_database("test_db")
    session = mongodb_client.start_session()

    try:
        with session.start_transaction():
            transactions_collection.insert_one({"name": "Alice", "balance": 100}, session=session)
            transactions_collection.insert_one({"name": "Bob", "balance": 50}, session=session)
            session.commit_transaction()
    finally:
        session.end_session()

    assert transactions_collection.count_documents({"name": "Alice"}) == 1
    assert transactions_collection.count_documents({"name": "Bob"}) == 1

