"""
04_performance_testing.py - Demonstrates Redis performance testing with Testcontainers.

This example measures the throughput of Redis commands under load.
"""

import pytest
import time

def test_redis_performance(redis_client):
    """Test Redis performance by measuring execution time for bulk insertions."""
    num_operations = 10000
    start_time = time.time()
    
    for i in range(num_operations):
        redis_client.set(f"key_{i}", f"value_{i}")
    
    duration = time.time() - start_time
    print(f"Inserted {num_operations} keys in {duration:.2f} seconds")
    
    assert duration < 10  # Expect the operations to complete within 10 seconds