"""
01_basic_crud.py - Basic CRUD operations with MongoDB and Testcontainers

This example demonstrates how to perform Create, Read, Update, and Delete (CRUD) operations
in a MongoDB container using Testcontainers.
"""

import pytest

def test_create_document(test_collection):
    """Test inserting a new document."""
    document = {"name": "Alice", "email": "alice@example.com", "phone": "123-456-7890"}
    result = test_collection.insert_one(document)
    assert result.inserted_id is not None

    # Verify the document was added
    saved_document = test_collection.find_one({"_id": result.inserted_id})
    assert saved_document["name"] == "Alice"
    assert saved_document["email"] == "alice@example.com"
    assert saved_document["phone"] == "123-456-7890"


def test_read_document(test_collection):
    """Test retrieving a document from the collection."""
    document = {"name": "Bob", "email": "bob@example.com", "phone": "987-654-3210"}
    test_collection.insert_one(document)

    # Verify the document can be read
    saved_document = test_collection.find_one({"email": "bob@example.com"})
    assert saved_document is not None
    assert saved_document["name"] == "Bob"
    assert saved_document["phone"] == "987-654-3210"


def test_update_document(test_collection):
    """Test updating an existing document."""
    document = {"name": "Charlie", "email": "charlie@example.com", "phone": "555-555-5555"}
    result = test_collection.insert_one(document)

    # Update the phone number
    test_collection.update_one(
        {"_id": result.inserted_id}, {"$set": {"phone": "111-111-1111"}}
    )

    # Verify the update
    updated_document = test_collection.find_one({"_id": result.inserted_id})
    assert updated_document["phone"] == "111-111-1111"


def test_delete_document(test_collection):
    """Test deleting a document from the collection."""
    document = {"name": "Dave", "email": "dave@example.com", "phone": "444-444-4444"}
    result = test_collection.insert_one(document)

    # Delete the document
    test_collection.delete_one({"_id": result.inserted_id})

    # Verify the document was deleted
    deleted_document = test_collection.find_one({"_id": result.inserted_id})
    assert deleted_document is None
