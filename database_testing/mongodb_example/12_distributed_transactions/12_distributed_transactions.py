"""
12_distributed_transactions.py - Testing Distributed Transactions

This example demonstrates how to test distributed transactions across multiple MongoDB databases
using a two-phase commit protocol simulation.
"""

import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def mongodb_container():
    """Start a MongoDB container as a replica set."""
    with MongoDbContainer("mongo:6.0") as mongo:
        # Wait for MongoDB to be ready
        time.sleep(5)  # Initial wait for MongoDB to start

        # Initialize the replica set
        mongo.exec(["mongo", "--eval", "rs.initiate()"])

        # Wait for the replica set to be ready
        timeout = 60  # Increase timeout to 60 seconds
        start_time = time.time()
        while True:
            try:
                # Check if the primary is available
                mongo.exec(["mongo", "--eval", "rs.status()"])
                logger.info("MongoDB replica set is ready.")
                break
            except Exception as e:
                logger.warning(f"MongoDB not ready yet: {e}")
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"MongoDB did not become ready in {timeout} seconds.")
                time.sleep(2)  # Wait before retrying

        yield mongo.get_connection_url()

@pytest.fixture(scope="module")
def mongodb_client(mongodb_container):
    """Create a MongoDB client connected to the replica set."""
    client = MongoClient(mongodb_container)
    yield client
    client.close()

def test_distributed_transaction(mongodb_client):
    """Test distributed transactions across multiple MongoDB databases."""
    db1 = mongodb_client.get_database("db1")
    db2 = mongodb_client.get_database("db2")

    # Start a session for transactions
    with mongodb_client.start_session() as session:
        try:
            with session.start_transaction():
                # Insert sample data into the first database
                db1.customers.insert_one({"customer_id": "C001", "name": "John Doe"}, session=session)
                logger.info("Inserted customer into db1: John Doe")

                # Insert sample data into the second database
                db2.orders.insert_one({"order_id": "O001", "customer_id": "C001", "amount": 100.0}, session=session)
                logger.info("Inserted order into db2: O001 for customer C001")

                # Simulate an error to trigger rollback
                raise Exception("Simulated error to trigger rollback")
        except Exception as e:
            logger.info(f"Transaction rolled back due to error: {e}")

    # Verify that no data was inserted due to rollback
    retrieved_customer_db1 = db1.customers.find_one({"customer_id": "C001"})
    retrieved_order_db2 = db2.orders.find_one({"order_id": "O001"})

    assert retrieved_customer_db1 is None, "Customer C001 should not exist in db1 after rollback."
    assert retrieved_order_db2 is None, "Order O001 should not exist in db2 after rollback."

def test_multiple_operations(mongodb_client):
    """Test multiple operations in a distributed transaction."""
    db1 = mongodb_client.get_database("db1")
    db2 = mongodb_client.get_database("db2")

    # Start a session for transactions
    with mongodb_client.start_session() as session:
        try:
            with session.start_transaction():
                # Insert multiple customers into the first database
                db1.customers.insert_many([
                    {"customer_id": "C002", "name": "Alice Smith"},
                    {"customer_id": "C003", "name": "Bob Johnson"}
                ], session=session)
                logger.info("Inserted multiple customers into db1.")

                # Insert multiple orders into the second database
                db2.orders.insert_many([
                    {"order_id": "O002", "customer_id": "C002", "amount": 150.0},
                    {"order_id": "O003", "customer_id": "C003", "amount": 200.0}
                ], session=session)
                logger.info("Inserted multiple orders into db2.")

                # Simulate an error to trigger rollback
                raise Exception("Simulated error to trigger rollback")
        except Exception as e:
            logger.info(f"Transaction rolled back due to error: {e}")

    # Verify that no data was inserted due to rollback
    retrieved_customers_db1 = list(db1.customers.find({"customer_id": {"$in": ["C002", "C003"]}}))
    retrieved_orders_db2 = list(db2.orders.find({"order_id": {"$in": ["O002", "O003"]}}))

    assert len(retrieved_customers_db1) == 0, "Customers C002 and C003 should not exist in db1 after rollback."
    assert len(retrieved_orders_db2) == 0, "Orders O002 and O003 should not exist in db2 after rollback."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
