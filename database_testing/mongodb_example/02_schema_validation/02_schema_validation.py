"""
02_schema_validation.py - Demonstrates schema validation in MongoDB with Testcontainers.

This example shows how to define and enforce a schema for a MongoDB collection using JSON schema validation.
"""

import pytest
from pymongo.errors import WriteError

def test_create_schema_validation(mongodb_client):
    """Test creating a schema validation rule for a collection."""
    db = mongodb_client.get_database("test_db")
    db.create_collection("validated_collection", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "email", "age"],
            "properties": {
                "name": {"bsonType": "string", "description": "must be a string and is required"},
                "email": {"bsonType": "string", "pattern": "^.+@.+$", "description": "must be a valid email"},
                "age": {"bsonType": "int", "minimum": 18, "description": "must be an integer >= 18"}
            }
        }
    })
    assert "validated_collection" in db.list_collection_names()


def test_valid_document_insertion(mongodb_client):
    """Test inserting a valid document into a schema-validated collection."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("validated_collection")
    document = {"name": "Alice", "email": "alice@example.com", "age": 25}
    result = collection.insert_one(document)
    assert result.inserted_id is not None


def test_invalid_document_insertion(mongodb_client):
    """Test inserting an invalid document that does not meet the schema constraints."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("validated_collection")
    invalid_document = {"name": "Bob", "email": "invalid-email", "age": 15}
    with pytest.raises(WriteError):
        collection.insert_one(invalid_document)