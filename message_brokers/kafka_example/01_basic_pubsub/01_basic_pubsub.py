"""
01_basic_pubsub.py - Demonstrates basic Kafka Pub/Sub with Testcontainers.

This example tests message publishing, consuming, and various messaging scenarios in Kafka.
"""

from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
import pytest
import time


@pytest.fixture(scope="module")
def kafka_bootstrap_server():
    """
    Starts a Kafka container and provides the bootstrap server URL for Kafka clients.
    """
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka.get_bootstrap_server()


def test_basic_pubsub(kafka_bootstrap_server):
    """
    Tests basic Kafka publish-subscribe functionality.
    """
    # Kafka topic name
    topic = "test_topic"

    # Produce a message to the Kafka topic
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    producer.send(topic, b"Hello, Kafka!")
    producer.flush()
    producer.close()

    # Allow some time for the message to be available
    time.sleep(2)

    # Consume the message from the Kafka topic
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_bootstrap_server,
        auto_offset_reset="earliest",
        group_id="test-group",
    )
    message = next(consumer)
    consumer.close()

    # Assert that the message received matches the sent message
    assert message.value == b"Hello, Kafka!"
