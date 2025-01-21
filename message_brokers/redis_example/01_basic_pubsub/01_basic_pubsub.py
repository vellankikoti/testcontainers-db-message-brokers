"""
01_basic_pubsub.py - Demonstrates basic Redis Pub/Sub with Testcontainers.

This example tests message publishing and subscribing in Redis.
"""

import pytest
import time

def test_redis_pubsub(redis_client):
    """Test that a message published to Redis is received by a subscriber."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe("test_channel")
    
    redis_client.publish("test_channel", "Hello, Redis!")
    
    time.sleep(2)  # Allow time for message propagation
    
    message = pubsub.get_message()
    assert message is not None
    assert message["type"] == "message"
    assert message["data"].decode("utf-8") == "Hello, Redis!"