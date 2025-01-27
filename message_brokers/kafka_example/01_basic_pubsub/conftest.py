"""
conftest.py - Shared Kafka fixture for Testcontainers.
"""

import pytest
import time
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="session")
def kafka_container():
    """Starts a Kafka container using Testcontainers and ensures it's ready."""
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        bootstrap_server = kafka.get_bootstrap_server()

        # ✅ Wait until Kafka is fully available
        max_wait_time = 30  # Max wait time in seconds
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_server)
                topics = admin_client.list_topics()
                if topics is not None:
                    break  # Kafka is ready
            except Exception:
                time.sleep(2)  # Retry every 2 seconds

        yield bootstrap_server  # Return Kafka connection string


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
