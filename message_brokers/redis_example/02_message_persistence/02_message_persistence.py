"""
02_message_persistence.py - Demonstrates Redis message persistence with Testcontainers.

This example verifies that Redis retains messages even after container restarts.
"""

import pytest
import time

def test_redis_message_persistence(redis_client, redis_container):
    """Test that messages persist in Redis even after a restart."""
    redis_client.set("persistent_key", "Persistent Value")
    
    redis_container.stop()
    time.sleep(5)  # Simulate downtime
    redis_container.start()
    time.sleep(5)  # Allow Redis to restart
    
    value = redis_client.get("persistent_key")
    assert value is not None
    assert value.decode("utf-8") == "Persistent Value"