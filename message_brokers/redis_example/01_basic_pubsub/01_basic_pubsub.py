"""
01_basic_pubsub.py - Demonstrates basic Redis Pub/Sub with Testcontainers.

This example tests message publishing and subscribing in Redis.
"""

import pytest
import time

def test_redis_pubsub(redis_client):
    """
    Test that a message published to Redis is received by a subscriber.

    Steps:
    1. Subscribe to a Redis channel.
    2. Skip the subscription confirmation message.
    3. Publish a message to the channel.
    4. Retrieve and validate the published message.
    """

    pubsub = redis_client.pubsub()
    pubsub.subscribe("test_channel")

    # **Skip the subscription confirmation message**
    time.sleep(1)
    pubsub.get_message()  # Discard the first 'subscribe' message

    # Publish a test message
    redis_client.publish("test_channel", "Hello, Redis!")

    # Wait for message propagation
    time.sleep(2)

    # Get the actual published message
    message = pubsub.get_message()

    assert message is not None, "No message received!"
    assert message["type"] == "message", f"Expected 'message', got {message['type']}"
    assert message["channel"] == "test_channel", "Incorrect channel!"
    assert message["data"] == "Hello, Redis!", "Incorrect message content!"

    print("\n✅ Redis Pub/Sub test passed successfully!")
