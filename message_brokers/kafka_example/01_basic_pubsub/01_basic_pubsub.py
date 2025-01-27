"""
01_basic_pubsub.py - Demonstrates basic Kafka Pub/Sub with Testcontainers.

This example tests message publishing, consuming, and various messaging scenarios in Kafka.
"""

import pytest
import time
from kafka import KafkaProducer, KafkaConsumer
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="module")
def kafka_container():
    """Starts a Kafka container using Testcontainers."""
    with KafkaContainer() as kafka:
        yield kafka.get_bootstrap_server()


@pytest.fixture
def kafka_producer(kafka_container):
    """Creates a Kafka producer."""
    producer = KafkaProducer(
        bootstrap_servers=kafka_container,
        value_serializer=lambda v: v.encode("utf-8"),
        acks="all",
        retries=5
    )
    yield producer
    producer.close()


@pytest.fixture
def kafka_consumer(kafka_container):
    """Creates a Kafka consumer."""
    consumer = KafkaConsumer(
        "test_topic",
        bootstrap_servers=kafka_container,
        value_deserializer=lambda x: x.decode("utf-8"),
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )
    yield consumer
    consumer.close()


def test_kafka_pub_sub(kafka_producer, kafka_consumer):
    """Test that a message published to Kafka is received by a consumer."""
    test_message = "Hello, Kafka!"
    kafka_producer.send("test_topic", test_message)
    kafka_producer.flush()

    time.sleep(2)  # Allow time for message propagation

    received_messages = [message.value for message in kafka_consumer]
    assert test_message in received_messages, "❌ Kafka message was not received!"


def test_kafka_multiple_messages(kafka_producer, kafka_consumer):
    """Test that multiple messages published to Kafka are received correctly."""
    messages = [f"Message {i}" for i in range(1, 6)]

    for msg in messages:
        kafka_producer.send("test_topic", msg)
    kafka_producer.flush()

    time.sleep(2)

    received_messages = [msg.value for msg in kafka_consumer]
    assert messages == received_messages, "❌ Kafka did not receive messages in order!"


def test_kafka_message_duplication(kafka_producer, kafka_consumer):
    """Ensure Kafka does not duplicate messages during normal operation."""
    unique_message = "Unique Kafka Message"
    kafka_producer.send("test_topic", unique_message)
    kafka_producer.send("test_topic", unique_message)
    kafka_producer.flush()

    time.sleep(2)

    received_messages = [msg.value for msg in kafka_consumer]
    assert received_messages.count(unique_message) == 2, "❌ Kafka duplicated messages!"


def test_kafka_replay_messages(kafka_producer, kafka_container):
    """Ensure Kafka can replay messages from the beginning."""
    topic = "test_topic_replay"
    test_messages = ["Replay 1", "Replay 2", "Replay 3"]

    for msg in test_messages:
        kafka_producer.send(topic, msg)
    kafka_producer.flush()

    time.sleep(2)

    # Create a new consumer to replay messages
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_container,
        value_deserializer=lambda x: x.decode("utf-8"),
        auto_offset_reset="earliest",
        enable_auto_commit=False  # Ensures messages are read from the beginning
    )

    received_messages = [msg.value for msg in consumer]
    assert received_messages == test_messages, "❌ Kafka failed to replay messages correctly!"
