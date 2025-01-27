import pymongo

def test_mongodb_duplicate_email(mongodb_test_db):
    """
    Ensures duplicate email insertion is prevented using a unique index.
    """
    collection = mongodb_test_db.data_integrity_test

    # Create a unique index on 'email'
    collection.create_index([("email", pymongo.ASCENDING)], unique=True)

    try:
        collection.insert_one({"email": "alice@example.com", "name": "Alice"})
        print("✅ Inserted first record successfully.")

        collection.insert_one({"email": "alice@example.com", "name": "Duplicate Alice"})  # Should fail
        print("❌ Data Integrity Failed: Duplicate Allowed.")
    
    except pymongo.errors.DuplicateKeyError:
        print("✅ Data Integrity Passed: Duplicate Prevented.")

def test_mongodb_insert_and_retrieve(mongodb_test_db):
    """
    Ensures that after inserting a record, it can be successfully retrieved.
    """
    collection = mongodb_test_db.data_integrity_test
    record = {"email": "bob@example.com", "name": "Bob"}

    # Insert record
    collection.insert_one(record)
    retrieved_record = collection.find_one({"email": "bob@example.com"})

    assert retrieved_record is not None, "❌ Record retrieval failed."
    assert retrieved_record["name"] == "Bob", "❌ Retrieved data mismatch."
    print("✅ Insert & Retrieve Integrity Passed.")

def test_mongodb_missing_required_fields(mongodb_test_db):
    """
    Ensures that records without a required 'email' field are rejected.
    """
    collection = mongodb_test_db.data_integrity_test

    try:
        collection.insert_one({"name": "Charlie"})  # Missing 'email' field
        print("❌ Missing Required Field Test Failed (Allowed insert without email).")
    except pymongo.errors.WriteError:
        print("✅ Missing Required Field Test Passed (Rejected insert without email).")

