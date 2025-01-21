"""
05_extended_stays.py - Extended Stay Management Test Suite

This module demonstrates testing extended stay functionality using MongoDB and Testcontainers.
It includes tests for extending reservations, calculating updated prices, and handling stay modifications.
"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta

# Test data
SAMPLE_ROOMS = [
    {"room_number": "101", "type": "Standard", "rate": 100.0, "status": "occupied"},
    {"room_number": "102", "type": "Deluxe", "rate": 150.0, "status": "available"},
    {"room_number": "103", "type": "Suite", "rate": 250.0, "status": "occupied"}
]

SAMPLE_RESERVATIONS = [
    {
        "reservation_id": "R001",
        "guest_name": "Alice",
        "room_number": "101",
        "check_in": datetime.now(),
        "check_out": datetime.now() + timedelta(days=3),
        "total_price": 300.0,
        "extensions": []
    }
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
def hotel_db(mongodb_client):
    """Set up the hotel database with rooms and reservations collections."""
    db = mongodb_client.get_database("hotel_db")

    # Clean up any existing data
    db.rooms.delete_many({})
    db.reservations.delete_many({})

    # Set up rooms collection
    rooms_collection = db.get_collection("rooms")
    rooms_collection.create_index([("room_number", ASCENDING)], unique=True)
    rooms_collection.insert_many(SAMPLE_ROOMS)

    # Set up reservations collection with fresh data for each test
    reservations_collection = db.get_collection("reservations")
    reservations_collection.create_index([("reservation_id", ASCENDING)], unique=True)
    reservations_collection.create_index([("room_number", ASCENDING), ("check_in", ASCENDING)])
    reservations_collection.insert_many(SAMPLE_RESERVATIONS)

    yield db

    # Cleanup after each test
    db.rooms.delete_many({})
    db.reservations.delete_many({})

def extend_stay(hotel_db, reservation_id: str, additional_days: int) -> bool:
    """Extend a guest's stay by the specified number of days."""
    # Find the reservation
    reservation = hotel_db.reservations.find_one({"reservation_id": reservation_id})
    if not reservation:
        return False

    # Get room rate
    room = hotel_db.rooms.find_one({"room_number": reservation["room_number"]})
    if not room:
        return False

    # Calculate extension details
    original_checkout = reservation["check_out"]
    new_checkout = original_checkout + timedelta(days=additional_days)
    additional_cost = room["rate"] * additional_days

    # Check if room is available for extension
    conflicting_reservation = hotel_db.reservations.find_one({
        "room_number": reservation["room_number"],
        "check_in": {"$lt": new_checkout},
        "check_out": {"$gt": original_checkout},
        "reservation_id": {"$ne": reservation_id}
    })

    if conflicting_reservation:
        return False

    # Update reservation
    extension = {
        "extended_on": datetime.now(),
        "original_checkout": original_checkout,
        "additional_days": additional_days,
        "additional_cost": additional_cost
    }

    result = hotel_db.reservations.update_one(
        {"reservation_id": reservation_id},
        {
            "$set": {
                "check_out": new_checkout,
                "total_price": reservation["total_price"] + additional_cost
            },
            "$push": {"extensions": extension}
        }
    )

    return result.modified_count > 0

def test_extend_stay_success(hotel_db):
    """Test successful extension of a stay."""
    # Extend Alice's stay by 2 days
    success = extend_stay(hotel_db, "R001", 2)
    assert success is True

    # Verify the extension
    reservation = hotel_db.reservations.find_one({"reservation_id": "R001"})
    assert len(reservation["extensions"]) == 1
    assert reservation["extensions"][0]["additional_days"] == 2
    assert reservation["extensions"][0]["additional_cost"] == 200.0
    assert reservation["total_price"] == 500.0  # Original 300 + 200 for extension

def test_extend_stay_conflict(hotel_db):
    """Test extension failure due to conflicting reservation."""
    # First, extend the stay once to set up the initial state
    initial_extension = extend_stay(hotel_db, "R001", 1)
    assert initial_extension is True

    # Add a conflicting future reservation
    conflicting_reservation = {
        "reservation_id": "R002",
        "guest_name": "Bob",
        "room_number": "101",
        "check_in": datetime.now() + timedelta(days=4),
        "check_out": datetime.now() + timedelta(days=6),
        "total_price": 200.0,
        "extensions": []
    }
    hotel_db.reservations.insert_one(conflicting_reservation)

    # Try to extend Alice's stay by 5 days (should fail)
    success = extend_stay(hotel_db, "R001", 5)
    assert success is False

    # Verify the original reservation remains unchanged
    reservation = hotel_db.reservations.find_one({"reservation_id": "R001"})
    assert len(reservation["extensions"]) == 1  # Still has only the first extension
    assert reservation["total_price"] == 400.0  # Original 300 + 100 for first extension

def test_multiple_extensions(hotel_db):
    """Test multiple extensions for the same reservation."""
    # First extension
    success1 = extend_stay(hotel_db, "R001", 1)
    assert success1 is True

    # Second extension
    success2 = extend_stay(hotel_db, "R001", 1)
    assert success2 is True

    # Verify both extensions
    reservation = hotel_db.reservations.find_one({"reservation_id": "R001"})
    assert len(reservation["extensions"]) == 2  # Should have exactly two extensions
    assert reservation["total_price"] == 500.0  # Original 300 + 200 for two extensions

    # Verify extension details
    extensions = reservation["extensions"]
    assert extensions[0]["additional_days"] == 1
    assert extensions[0]["additional_cost"] == 100.0
    assert extensions[1]["additional_days"] == 1
    assert extensions[1]["additional_cost"] == 100.0

def test_invalid_reservation(hotel_db):
    """Test extending a non-existent reservation."""
    success = extend_stay(hotel_db, "INVALID", 1)
    assert success is False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
