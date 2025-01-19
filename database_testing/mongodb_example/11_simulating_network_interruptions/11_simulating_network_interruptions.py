"""
11_simulating_network_interruptions.py - Simulating Network Interruptions

This example demonstrates how to simulate network interruptions while interacting with a MongoDB database.
"""

import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer
import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container."""
    with MongoDbContainer("mongo:6.0") as mongo:
        yield mongo.get_connection_url()

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the container."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()

def simulate_network_interruption():
    """Simulate a network interruption randomly."""
    if random.choice([True, False]):
        logger.info("Simulating network interruption...")
        time.sleep(2)  # Simulate a delay
        raise ConnectionError("Simulated network interruption occurred.")

def test_network_interruption_handling(mongodb_client):
    """Test handling of network interruptions during database operations."""
    db = mongodb_client.get_database("test_db")
    collection = db.get_collection("customers")

    # Insert sample data into MongoDB
    sample_data = [
        {"customer_id": "C001", "name": "John Doe", "email": "john@example.com"},
        {"customer_id": "C002", "name": "Jane Smith", "email": "jane@example.com"},
    ]

    for customer in sample_data:
        success = False
        while not success:
            try:
                simulate_network_interruption()  # Simulate potential network interruption
                collection.insert_one(customer)
                logger.info(f"Inserted customer: {customer}")
                success = True  # Mark success if insertion is successful
            except ConnectionError as e:
                logger.error(f"Failed to insert customer due to network issue: {e}")
                time.sleep(1)  # Wait before retrying

    # Verify data in MongoDB
    for customer in sample_data:
        retrieved_customer = collection.find_one({"customer_id": customer["customer_id"]})
        assert retrieved_customer is not None, f"Customer {customer['customer_id']} not found in database."
        assert retrieved_customer["name"] == customer["name"], f"Expected name {customer['name']} but got {retrieved_customer['name']}."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
