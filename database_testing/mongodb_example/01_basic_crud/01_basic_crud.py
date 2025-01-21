"""
01_basic_guests.py - Basic Guest Registration System

This example demonstrates a basic guest registration system using MongoDB and Testcontainers.
It performs CRUD operations on a MongoDB collection to manage guest data.
"""

def test_create_guest(guests_collection):
    """Test creating a new guest."""
    guest = {"name": "Alice", "email": "alice@example.com", "phone": "123-456-7890"}
    result = guests_collection.insert_one(guest)
    assert result.inserted_id is not None

    # Verify the guest was added
    saved_guest = guests_collection.find_one({"_id": result.inserted_id})
    assert saved_guest["name"] == "Alice"
    assert saved_guest["email"] == "alice@example.com"
    assert saved_guest["phone"] == "123-456-7890"


def test_read_guest(guests_collection):
    """Test reading a guest's details."""
    guest = {"name": "Bob", "email": "bob@example.com", "phone": "987-654-3210"}
    guests_collection.insert_one(guest)

    # Verify the guest can be read
    saved_guest = guests_collection.find_one({"email": "bob@example.com"})
    assert saved_guest is not None
    assert saved_guest["name"] == "Bob"
    assert saved_guest["phone"] == "987-654-3210"


def test_update_guest(guests_collection):
    """Test updating a guest's details."""
    guest = {"name": "Charlie", "email": "charlie@example.com", "phone": "555-555-5555"}
    result = guests_collection.insert_one(guest)

    # Update the guest's phone number
    guests_collection.update_one(
        {"_id": result.inserted_id}, {"$set": {"phone": "111-111-1111"}}
    )

    # Verify the update
    updated_guest = guests_collection.find_one({"_id": result.inserted_id})
    assert updated_guest["phone"] == "111-111-1111"


def test_delete_guest(guests_collection):
    """Test deleting a guest."""
    guest = {"name": "Dave", "email": "dave@example.com", "phone": "444-444-4444"}
    result = guests_collection.insert_one(guest)

    # Delete the guest
    guests_collection.delete_one({"_id": result.inserted_id})

    # Verify the guest was deleted
    deleted_guest = guests_collection.find_one({"_id": result.inserted_id})
    assert deleted_guest is None
