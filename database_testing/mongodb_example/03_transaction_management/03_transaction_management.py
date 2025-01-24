def test_transaction_commit(mongodb_client):
    """
    Tests MongoDB transactions by committing multiple operations.
    """
    db = mongodb_client["test_db"]
    users_collection = db["users"]
    session = mongodb_client.start_session()

    try:
        # Start Transaction
        session.start_transaction()

        # Insert Data
        users_collection.insert_one({"name": "Alice", "email": "alice@example.com"}, session=session)
        users_collection.insert_one({"name": "Bob", "email": "bob@example.com"}, session=session)

        # Update Data
        users_collection.update_one({"name": "Alice"}, {"$set": {"email": "alice@updated.com"}}, session=session)

        # Commit Transaction
        session.commit_transaction()

        # Validate that data is persisted
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
        # Start Transaction
        session.start_transaction()

        # Insert Data
        users_collection.insert_one({"name": "Charlie", "email": "charlie@example.com"}, session=session)

        # Rollback Transaction
        session.abort_transaction()

        # Validate that Charlie does not exist (rollback successful)
        assert users_collection.find_one({"name": "Charlie"}) is None

    finally:
        session.end_session()
