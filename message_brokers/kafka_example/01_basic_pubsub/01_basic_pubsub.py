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


def test_basic_pubsub_single_message(kafka_bootstrap_server):
    """
    Tests basic Kafka publish-subscribe functionality for a single message.
    """
    topic = "test_topic"

    # Produce a single message
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    producer.send(topic, b"Hello, Kafka!")
    producer.flush()
    producer.close()

    # Allow time for the message to be available
    time.sleep(2)

    # Consume the message
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_bootstrap_server,
        auto_offset_reset="earliest",
        group_id="test-group",
    )
    message = next(consumer)
    consumer.close()

    # Assert that the received message matches the sent message
    assert message.value == b"Hello, Kafka!"


def test_basic_pubsub_multiple_messages(kafka_bootstrap_server):
    """
    Tests Kafka publish-subscribe functionality for multiple messages.
    """
    topic = "test_topic_multi"

    # Messages to send
    messages_to_send = [b"Message 1", b"Message 2", b"Message 3"]

    # Produce multiple messages
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    for msg in messages_to_send:
        producer.send(topic, msg)
    producer.flush()
    producer.close()

    # Allow time for messages to be available
    time.sleep(2)

    # Consume messages
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_bootstrap_server,
        auto_offset_reset="earliest",
        group_id="test-group-multi",
    )

    received_messages = [msg.value for msg in consumer]
    consumer.close()

    # Assert that all sent messages are received
    assert received_messages == messages_to_send
