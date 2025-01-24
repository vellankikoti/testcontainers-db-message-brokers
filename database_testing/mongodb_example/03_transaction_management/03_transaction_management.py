def test_transaction_commit(mongodb_client):
    db = mongodb_client.test_database
    collection = db.test_collection

    # Start session and transaction
    with mongodb_client.start_session() as session:
        with session.start_transaction():
            collection.insert_one({"key": "value"}, session=session)
    
    assert collection.count_documents({}) == 1


def test_transaction_rollback(mongodb_client):
    db = mongodb_client.test_database
    collection = db.test_collection

    # Start session and transaction
    with mongodb_client.start_session() as session:
        with session.start_transaction():
            collection.insert_one({"key": "temp_value"}, session=session)
            session.abort_transaction()  # Rollback

    assert collection.count_documents({"key": "temp_value"}) == 0
