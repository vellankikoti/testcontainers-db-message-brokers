"""
04_performance_testing.py - Demonstrates performance testing in MongoDB with Testcontainers.

This example shows how to measure query execution time and optimize database operations.
"""

import pytest
import time

def test_bulk_insert_performance(test_collection):
    """Test bulk insertion performance by inserting 10,000 documents."""
    documents = [{"name": f"User{i}", "email": f"user{i}@example.com", "age": i % 50} for i in range(10000)]
    
    start_time = time.time()
    test_collection.insert_many(documents)
    execution_time = time.time() - start_time
    
    assert test_collection.count_documents({}) == 10000
    print(f"Bulk insert execution time: {execution_time:.4f} seconds")


def test_indexed_query_performance(test_collection):
    """Test query execution time before and after indexing."""
    test_collection.create_index("email")
    
    start_time = time.time()
    list(test_collection.find({"email": "user5000@example.com"}))
    execution_time_with_index = time.time() - start_time
    
    assert execution_time_with_index < 0.01
    print(f"Indexed query execution time: {execution_time_with_index:.4f} seconds")