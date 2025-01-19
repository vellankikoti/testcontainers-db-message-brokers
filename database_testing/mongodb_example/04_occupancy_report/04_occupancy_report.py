"""
04_occupancy_report.py - Occupancy Report Test Suite

This module demonstrates testing occupancy reporting functionality using MongoDB and Testcontainers.
"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta
from typing import Dict

# Test data - Changed Decimal to float
SAMPLE_ROOMS = [
    {"room_number": "101", "type": "Standard", "rate": 100.0, "status": "occupied"},
    {"room_number": "102", "type": "Deluxe", "rate": 150.0, "status": "available"},
    {"room_number": "103", "type": "Suite", "rate": 250.0, "status": "occupied"},
    {"room_number": "201", "type": "Standard", "rate": 100.0, "status": "available"},
    {"room_number": "202", "type": "Deluxe", "rate": 150.0, "status": "maintenance"},
]

SAMPLE_RESERVATIONS = [
    {
        "guest_name": "Alice",
        "room_number": "101",
        "check_in": datetime.now(),
        "check_out": datetime.now() + timedelta(days=2),
        "total_price": 200.0,  # Changed from Decimal to float
    },
    {
        "guest_name": "Bob",
        "room_number": "103",
        "check_in": datetime.now(),
        "check_out": datetime.now() + timedelta(days=3),
        "total_price": 750.0,  # Changed from Decimal to float
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
def hotel_db(mongodb_client):
    """Set up the hotel database with rooms and reservations collections."""
    db = mongodb_client.get_database("hotel_db")
    
    # Set up rooms collection
    rooms_collection = db.get_collection("rooms")
    rooms_collection.create_index([("room_number", ASCENDING)], unique=True)
    rooms_collection.insert_many(SAMPLE_ROOMS)
    
    # Set up reservations collection
    reservations_collection = db.get_collection("reservations")
    reservations_collection.create_index([("room_number", ASCENDING), ("check_in", ASCENDING)])
    reservations_collection.insert_many(SAMPLE_RESERVATIONS)
    
    yield db
    
    # Cleanup
    rooms_collection.delete_many({})
    reservations_collection.delete_many({})

def calculate_occupancy_rate(hotel_db) -> float:
    """Calculate current occupancy rate."""
    total_rooms = hotel_db.rooms.count_documents({})
    occupied_rooms = hotel_db.rooms.count_documents({"status": "occupied"})
    return (occupied_rooms / total_rooms) * 100 if total_rooms > 0 else 0

def get_room_type_availability(hotel_db) -> Dict[str, Dict[str, int]]:
    """Get availability counts by room type."""
    pipeline = [
        {"$group": {
            "_id": {
                "type": "$type",
                "status": "$status"
            },
            "count": {"$sum": 1}
        }}
    ]
    results = list(hotel_db.rooms.aggregate(pipeline))
    
    availability = {}
    for result in results:
        room_type = result["_id"]["type"]
        status = result["_id"]["status"]
        if room_type not in availability:
            availability[room_type] = {"available": 0, "occupied": 0, "maintenance": 0}
        availability[room_type][status] = result["count"]
    
    return availability

def calculate_daily_revenue(hotel_db, date: datetime) -> float:
    """Calculate total revenue for a specific date."""
    pipeline = [
        {"$match": {
            "check_in": {"$lte": date},
            "check_out": {"$gt": date}
        }},
        {"$lookup": {
            "from": "rooms",
            "localField": "room_number",
            "foreignField": "room_number",
            "as": "room"
        }},
        {"$unwind": "$room"},
        {"$group": {
            "_id": None,
            "total_revenue": {"$sum": "$room.rate"}
        }}
    ]
    result = list(hotel_db.reservations.aggregate(pipeline))
    return float(result[0]["total_revenue"]) if result else 0.0

def test_occupancy_rate(hotel_db):
    """Test calculating current occupancy rate."""
    occupancy_rate = calculate_occupancy_rate(hotel_db)
    assert occupancy_rate == 40.0  # 2 out of 5 rooms are occupied

def test_room_type_availability(hotel_db):
    """Test room type availability reporting."""
    availability = get_room_type_availability(hotel_db)
    
    # Verify Standard rooms
    assert availability["Standard"]["occupied"] == 1
    assert availability["Standard"]["available"] == 1
    
    # Verify Deluxe rooms
    assert availability["Deluxe"]["available"] == 1
    assert availability["Deluxe"]["maintenance"] == 1
    
    # Verify Suite rooms
    assert availability["Suite"]["occupied"] == 1

def test_daily_revenue(hotel_db):
    """Test daily revenue calculation."""
    today = datetime.now()
    revenue = calculate_daily_revenue(hotel_db, today)
    assert revenue == 350.0  # 100 (Standard) + 250 (Suite)

def test_future_occupancy(hotel_db):
    """Test future occupancy prediction."""
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Add future reservation
    future_reservation = {
        "guest_name": "Charlie",
        "room_number": "102",
        "check_in": tomorrow,
        "check_out": tomorrow + timedelta(days=1),
        "total_price": 150.0,  # Changed from Decimal to float
    }
    hotel_db.reservations.insert_one(future_reservation)
    
    # Calculate future revenue
    future_revenue = calculate_daily_revenue(hotel_db, tomorrow)
    assert future_revenue == 500.0  # 100 (Standard) + 250 (Suite) + 150 (Deluxe)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
