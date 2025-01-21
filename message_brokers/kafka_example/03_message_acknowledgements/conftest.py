"""
conftest.py - Shared fixtures for Kafka example
"""

import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
import time

@pytest.fixture(scope="module")
def kafka_container():
    """Start a Kafka container and provide the connection details."""
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka

@pytest.fixture(scope="module")
def kafka_producer(kafka_container):
    """Set up a Kafka producer."""
    producer = KafkaProducer(
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        value_serializer=lambda v: v.encode('utf-8')
    )
    yield producer
    producer.close()

@pytest.fixture(scope="module")
def kafka_consumer(kafka_container):
    """Set up a Kafka consumer."""
    consumer = KafkaConsumer(
        "test_topic",
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    yield consumer
    consumer.close()