"""
01_basic_pubsub.py - Demonstrates basic Kafka Pub/Sub with Testcontainers.

This example tests message publishing and consuming in Kafka.
"""

import pytest
import time

def test_kafka_pub_sub(kafka_producer, kafka_consumer):
    """Test that a message published to Kafka is received by a consumer."""
    test_message = "Hello, Kafka!"
    kafka_producer.send("test_topic", test_message)
    kafka_producer.flush()
    
    time.sleep(2)  # Allow time for message propagation
    
    for message in kafka_consumer:
        assert message.value == test_message
        break  # Exit after first message