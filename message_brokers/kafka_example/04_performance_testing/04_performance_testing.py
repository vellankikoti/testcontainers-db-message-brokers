"""
04_performance_testing.py - Demonstrates Kafka performance testing with Testcontainers.

This example measures Kafka message throughput under high load.
"""

import pytest
import time

def test_kafka_producer_performance(kafka_producer):
    """Test Kafka producer performance by sending multiple messages."""
    num_messages = 10000
    start_time = time.time()
    for i in range(num_messages):
        kafka_producer.send("test_topic", f"Message {i}")
    kafka_producer.flush()
    duration = time.time() - start_time
    print(f"Sent {num_messages} messages in {duration:.2f} seconds")
    assert duration < 10  # Expect all messages to be sent within 10 seconds

def test_kafka_consumer_performance(kafka_consumer):
    """Test Kafka consumer performance by consuming multiple messages."""
    start_time = time.time()
    count = 0
    for message in kafka_consumer:
        count += 1
        if count >= 10000:
            break
    duration = time.time() - start_time
    print(f"Consumed {count} messages in {duration:.2f} seconds")
    assert duration < 15  # Expect all messages to be consumed within 15 seconds