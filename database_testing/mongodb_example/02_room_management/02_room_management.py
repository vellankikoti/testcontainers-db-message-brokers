"""
02_room_management.py - Room Management System Test Suite

This module demonstrates testing room management functionality using MongoDB and Testcontainers.
It includes tests for creating, reading, updating, and deleting room records, as well as
room availability and pricing operations.
"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta
from bson import ObjectId

# Test data
SAMPLE_ROOMS = [
    {"room_number": "101", "type": "Standard", "rate": 100.00, "status": "available"},
    {"room_number": "102", "type": "Deluxe", "rate": 150.00, "status": "available"},
    {"room_number": "201", "type": "Suite", "rate": 250.00, "status": "available"},
    {"room_number": "202", "type": "Standard", "rate": 100.00, "status": "maintenance"},
]

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container and provide the connection URL."""
    with MongoDbContainer("mongo:6.0") as mongo:
        yield mongo.get_connection_url()

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()

@pytest.fixture(scope="function")
def rooms_collection(mongodb_client):
    """Set up the 'rooms' collection in the MongoDB database."""
    db = mongodb_client.get_database("hotel_db")
    collection = db.get_collection("rooms")

    # Create index on room_number for faster lookups
    collection.create_index([("room_number", ASCENDING)], unique=True)

    # Insert sample room data
    collection.insert_many(SAMPLE_ROOMS)

    yield collection

    # Cleanup after tests
    collection.delete_many({})

def test_create_room(rooms_collection):
    """Test creating a new room."""
    new_room = {
        "room_number": "301",
        "type": "Penthouse",
        "rate": 500.00,
        "status": "available"
    }

    result = rooms_collection.insert_one(new_room)
    assert result.inserted_id is not None

    # Verify the room was created
    saved_room = rooms_collection.find_one({"room_number": "301"})
    assert saved_room is not None
    assert saved_room["type"] == "Penthouse"
    assert saved_room["rate"] == 500.00

def test_read_room(rooms_collection):
    """Test reading room details."""
    room = rooms_collection.find_one({"room_number": "101"})
    assert room is not None
    assert room["type"] == "Standard"
    assert room["rate"] == 100.00
    assert room["status"] == "available"

def test_update_room(rooms_collection):
    """Test updating room details."""
    # Update room rate
    result = rooms_collection.update_one(
        {"room_number": "102"},
        {"$set": {"rate": 175.00}}
    )
    assert result.modified_count == 1

    # Verify the update
    updated_room = rooms_collection.find_one({"room_number": "102"})
    assert updated_room["rate"] == 175.00

def test_delete_room(rooms_collection):
    """Test deleting a room."""
    result = rooms_collection.delete_one({"room_number": "201"})
    assert result.deleted_count == 1

    # Verify the room was deleted
    deleted_room = rooms_collection.find_one({"room_number": "201"})
    assert deleted_room is None

def test_room_availability(rooms_collection):
    """Test querying room availability."""
    available_rooms = list(rooms_collection.find({"status": "available"}))
    assert len(available_rooms) == 3  # Initially 3 rooms are available

    # Change room status to occupied
    rooms_collection.update_one(
        {"room_number": "101"},
        {"$set": {"status": "occupied"}}
    )

    # Verify available rooms count
    available_rooms = list(rooms_collection.find({"status": "available"}))
    assert len(available_rooms) == 2

def test_room_pricing(rooms_collection):
    """Test room pricing operations."""
    # Test average rate by room type
    pipeline = [
        {"$match": {"status": "available"}},
        {"$group": {
            "_id": "$type",
            "avg_rate": {"$avg": "$rate"}
        }}
    ]

    results = list(rooms_collection.aggregate(pipeline))
    for result in results:
        if result["_id"] == "Standard":
            assert result["avg_rate"] == 100.00
        elif result["_id"] == "Deluxe":
            assert result["avg_rate"] == 150.00

def test_maintenance_status(rooms_collection):
    """Test handling rooms under maintenance."""
    # Find rooms under maintenance
    maintenance_rooms = list(rooms_collection.find({"status": "maintenance"}))
    assert len(maintenance_rooms) == 1
    assert maintenance_rooms[0]["room_number"] == "202"

    # Mark room as available after maintenance
    rooms_collection.update_one(
        {"room_number": "202"},
        {"$set": {"status": "available"}}
    )

    # Verify status change
    updated_room = rooms_collection.find_one({"room_number": "202"})
    assert updated_room["status"] == "available"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
