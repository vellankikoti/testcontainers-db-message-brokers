"""
03_transaction_management.py - Demonstrates transaction management in MongoDB with Testcontainers.

This example shows how to use MongoDB transactions to ensure atomicity in multi-operation scenarios.
"""

import pytest
from pymongo.errors import OperationFailure

# Fix Import Issue
try:
    from conftest import wait_for_primary
except ImportError:
    import sys
    sys.path.append("..")  # Add parent directory to Python path
    from conftest import wait_for_primary  # Import after fixing path


def test_transaction_commit(mongodb_client, transactions_collection):
    """Test a successful transaction commit."""
    wait_for_primary(mongodb_client)  # Ensure PRIMARY node is active before starting

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


def test_transaction_rollback(mongodb_client, transactions_collection):
    """Test a transaction rollback scenario."""
    wait_for_primary(mongodb_client)  # Ensure PRIMARY node is active before starting

    db = mongodb_client.get_database("test_db")
    session = mongodb_client.start_session()

    try:
        with pytest.raises(OperationFailure):
            with session.start_transaction():
                transactions_collection.insert_one({"name": "Charlie", "balance": 200}, session=session)
                raise OperationFailure("Simulating a failure")
                session.commit_transaction()
    finally:
        session.end_session()

    assert transactions_collection.count_documents({"name": "Charlie"}) == 0
