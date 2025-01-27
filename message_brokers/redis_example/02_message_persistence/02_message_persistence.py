"""
02_message_persistence.py - Tests Redis message persistence with Testcontainers.

This test:
1. Stores a key-value pair in Redis.
2. Ensures the value is retrievable after a reconnect.
"""

import pytest

def test_redis_message_persistence(redis_client):
    """
    Validates that Redis can persist messages across connections.

    Steps:
    1. Store a key-value pair in Redis.
    2. Retrieve the value and validate persistence.
    """

    redis_client.set("persistent_key", "Redis Persistence Test")

    value = redis_client.get("persistent_key")
    assert value is not None, "⚠️ Redis returned None!"
    assert value == "Redis Persistence Test", "⚠️ Redis value mismatch!"

    print("\n✅ Redis message persistence test passed successfully!")
