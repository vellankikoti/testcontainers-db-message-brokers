"""
05_resilience_testing.py - Demonstrates Redis resilience testing with Testcontainers.

This example tests Redis durability and reconnection handling after failures.
"""

import pytest
import time

def test_redis_resilience(redis_client, redis_container):
    """Test Redis resilience by setting a key, restarting Redis, and verifying persistence."""
    redis_client.set("resilient_key", "Resilient Value")
    
    # Stop Redis to simulate failure
    redis_container.stop()
    time.sleep(5)  # Simulate downtime
    
    # Restart Redis
    redis_container.start()
    time.sleep(5)  # Allow Redis to restart
    
    value = redis_client.get("resilient_key")
    assert value is not None
    assert value.decode("utf-8") == "Resilient Value"