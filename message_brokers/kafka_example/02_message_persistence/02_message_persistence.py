"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.
"""

import pytest
import time

def test_kafka_message_persistence(kafka_producer, kafka_consumer, kafka_container):
    """Test that messages remain in Kafka even after a restart."""
    test_message = "Persistent Message"
    kafka_producer.send("test_topic", test_message)
    kafka_producer.flush()
    
    kafka_container.stop()
    time.sleep(5)  # Simulate downtime
    kafka_container.start()
    time.sleep(5)  # Allow Kafka to restart
    
    for message in kafka_consumer:
        assert message.value == test_message
        break  # Exit after verifying the first message