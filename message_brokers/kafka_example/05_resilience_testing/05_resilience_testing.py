"""
05_resilience_testing.py - Demonstrates Kafka resilience testing with Testcontainers.

This example tests Kafka message durability and reconnection handling after failures.
"""

import pytest
import time

def test_kafka_resilience(kafka_producer, kafka_consumer, kafka_container):
    """Test Kafka resilience by sending messages, restarting Kafka, and verifying message persistence."""
    test_message = "Resilient Message"
    kafka_producer.send("test_topic", test_message)
    kafka_producer.flush()
    
    # Stop Kafka to simulate failure
    kafka_container.stop()
    time.sleep(5)  # Simulate downtime
    
    # Restart Kafka
    kafka_container.start()
    time.sleep(5)  # Allow Kafka to restart
    
    for message in kafka_consumer:
        assert message.value == test_message
        break  # Exit after verifying the first message