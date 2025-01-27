"""
conftest.py - Shared Kafka fixture using Testcontainers.
"""

import pytest
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope="module")
def kafka_container():
    """Starts a Kafka container and provides the bootstrap server URL."""
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka.get_bootstrap_server()


# File: 01_basic_pubsub.py

from kafka import KafkaProducer, KafkaConsumer
import time
import pytest

def test_basic_pubsub(kafka_container):
    """Tests basic Kafka publish-subscribe using Testcontainers."""
    topic = "test_topic"
    message = b"Hello, Kafka!"
    
    # Kafka Producer
    producer = KafkaProducer(bootstrap_servers=kafka_container)
    producer.send(topic, message)
    producer.flush()
    
    # Kafka Consumer
    consumer = KafkaConsumer(
        topic, 
        bootstrap_servers=kafka_container, 
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=5000  # Timeout in case no message is received
    )
    
    received_message = next(consumer)
    assert received_message.value == message, "Kafka message mismatch!"
