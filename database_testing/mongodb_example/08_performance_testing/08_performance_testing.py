"""
08_performance_testing.py - Performance Testing with MongoDB

This example demonstrates how to use Testcontainers to conduct performance testing on MongoDB.
It includes:
- Measuring query execution times.
- Analyzing the impact of indexing.
- Testing read and write operations under load.
"""

import pytest
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def performance_db(mongo_client):
    """Set up the performance testing database."""
    db = mongo_client.get_database("performance_db")

    # Clean up any existing data
    db.records.delete_many({})

    # Insert sample data
    logger.info("Inserting sample data...")
    sample_data = [{"record_id": i, "value": random.randint(1, 1000)} for i in range(10000)]
    db.records.insert_many(sample_data)

    yield db

    # Cleanup after tests
    logger.info("Cleaning up test data...")
    db.records.delete_many({})

def test_read_performance(performance_db):
    """Test read performance."""
    logger.info("Testing read performance...")
    start_time = time.time()

    # Perform a query
    results = list(performance_db.records.find({"value": {"$gt": 500}}))
    end_time = time.time()

    logger.info(f"Read performance test completed in {end_time - start_time:.4f} seconds")
    assert len(results) > 0

def test_write_performance(performance_db):
    """Test write performance."""
    logger.info("Testing write performance...")
    start_time = time.time()

    # Insert new records
    new_records = [{"record_id": i, "value": random.randint(1, 1000)} for i in range(10000, 20000)]
    performance_db.records.insert_many(new_records)
    end_time = time.time()

    logger.info(f"Write performance test completed in {end_time - start_time:.4f} seconds")
    assert performance_db.records.count_documents({}) >= 20000

def test_indexing_performance(performance_db):
    """Test the impact of indexing on query performance."""
    logger.info("Testing indexing performance...")

    # Create an index
    logger.info("Creating index on 'value' field...")
    performance_db.records.create_index("value")

    # Measure query time with index
    start_time = time.time()
    results = list(performance_db.records.find({"value": {"$gt": 500}}))
    end_time = time.time()

    logger.info(f"Query with index completed in {end_time - start_time:.4f} seconds")
    assert len(results) > 0

def test_concurrent_operations(performance_db):
    """Test concurrent read and write operations."""
    logger.info("Testing concurrent operations...")

    def write_operation():
        for i in range(20000, 30000):
            performance_db.records.insert_one({"record_id": i, "value": random.randint(1, 1000)})

    def read_operation():
        for _ in range(100):
            list(performance_db.records.find({"value": {"$gt": 500}}))

    # Perform concurrent operations
    from threading import Thread
    writer = Thread(target=write_operation)
    reader = Thread(target=read_operation)

    start_time = time.time()
    writer.start()
    reader.start()
    writer.join()
    reader.join()
    end_time = time.time()

    logger.info(f"Concurrent operations completed in {end_time - start_time:.4f} seconds")
    assert performance_db.records.count_documents({}) >= 30000

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
