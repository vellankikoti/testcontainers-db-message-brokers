"""
03_reservations.py - Reservation Management System Test Suite

This module demonstrates testing reservation management functionality using MongoDB and Testcontainers.
It includes tests for creating, reading, updating, and deleting reservations, as well as
validating constraints like overlapping reservations.
"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta

# Test data
SAMPLE_RESERVATIONS = [
    {
        "guest_name": "Alice",
        "room_number": "101",
        "check_in": datetime.now(),  # Changed from date() to datetime
        "check_out": (datetime.now() + timedelta(days=2)),  # Changed from date() to datetime
        "total_price": 200.00,
    },
    {
        "guest_name": "Bob",
        "room_number": "102",
        "check_in": datetime.now(),  # Changed from date() to datetime
        "check_out": (datetime.now() + timedelta(days=3)),  # Changed from date() to datetime
        "total_price": 450.00,
    },
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
def reservations_collection(mongodb_client):
    """Set up the 'reservations' collection in the MongoDB database."""
    db = mongodb_client.get_database("hotel_db")
    collection = db.get_collection("reservations")

    # Create index on room_number and check_in for faster lookups
    collection.create_index([("room_number", ASCENDING), ("check_in", ASCENDING)])

    # Insert sample reservation data
    collection.insert_many(SAMPLE_RESERVATIONS)

    yield collection

    # Cleanup after tests
    collection.delete_many({})

def test_create_reservation(reservations_collection):
    """Test creating a new reservation."""
    new_reservation = {
        "guest_name": "Charlie",
        "room_number": "201",
        "check_in": datetime.now(),  # Changed from date() to datetime
        "check_out": (datetime.now() + timedelta(days=1)),  # Changed from date() to datetime
        "total_price": 150.00,
    }

    result = reservations_collection.insert_one(new_reservation)
    assert result.inserted_id is not None

    # Verify the reservation was created
    saved_reservation = reservations_collection.find_one({"guest_name": "Charlie"})
    assert saved_reservation is not None
    assert saved_reservation["room_number"] == "201"
    assert saved_reservation["total_price"] == 150.00

def test_read_reservation(reservations_collection):
    """Test reading reservation details."""
    reservation = reservations_collection.find_one({"guest_name": "Alice"})
    assert reservation is not None
    assert reservation["room_number"] == "101"
    assert reservation["total_price"] == 200.00

def test_update_reservation(reservations_collection):
    """Test updating reservation details."""
    # Update total price
    result = reservations_collection.update_one(
        {"guest_name": "Bob"},
        {"$set": {"total_price": 500.00}}
    )
    assert result.modified_count == 1

    # Verify the update
    updated_reservation = reservations_collection.find_one({"guest_name": "Bob"})
    assert updated_reservation["total_price"] == 500.00

def test_delete_reservation(reservations_collection):
    """Test deleting a reservation."""
    result = reservations_collection.delete_one({"guest_name": "Alice"})
    assert result.deleted_count == 1

    # Verify the reservation was deleted
    deleted_reservation = reservations_collection.find_one({"guest_name": "Alice"})
    assert deleted_reservation is None

def test_overlapping_reservations(reservations_collection):
    """Test preventing overlapping reservations."""
    overlapping_reservation = {
        "guest_name": "Eve",
        "room_number": "101",
        "check_in": datetime.now(),  # Changed from date() to datetime
        "check_out": (datetime.now() + timedelta(days=1)),  # Changed from date() to datetime
        "total_price": 100.00,
    }

    # Check for overlapping reservations
    existing_reservation = reservations_collection.find_one({
        "room_number": overlapping_reservation["room_number"],
        "check_in": {"$lt": overlapping_reservation["check_out"]},
        "check_out": {"$gt": overlapping_reservation["check_in"]}
    })

    assert existing_reservation is not None, "Should detect overlapping reservation"

def test_reservation_duration(reservations_collection):
    """Test calculating reservation duration."""
    reservation = reservations_collection.find_one({"guest_name": "Bob"})
    check_in = reservation["check_in"]
    check_out = reservation["check_out"]

    duration = (check_out - check_in).days
    assert duration == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
