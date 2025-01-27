"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.
"""

import time
import pytest
from kafka import KafkaProducer, KafkaConsumer
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="module")
def kafka_container():
    """
    Pytest fixture to start a Kafka container.

    Returns:
        str: Bootstrap server URL of the running Kafka container.
    """
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka.get_bootstrap_server()


def test_kafka_message_persistence(kafka_container):
    """
    Test case to validate Kafka message persistence across broker restarts.

    Steps:
        1. Start a Kafka container.
        2. Produce a message to a Kafka topic.
        3. Stop and restart the Kafka container.
        4. Consume the message from the same topic after restart.
        5. Assert that the message is still available after Kafka restart.
    """
    topic = "test_topic"

    # Step 1: Produce messages before stopping Kafka
    print("\nProducing message to Kafka topic...")
    producer = KafkaProducer(bootstrap_servers=kafka_container)
    producer.send(topic, b"Persistent Message")
    producer.flush()
    print("Message produced successfully!")

    # Step 2: Stop Kafka container
    print("\nStopping Kafka container...")
    kafka_container_obj = KafkaContainer("confluentinc/cp-kafka:latest")
    kafka_container_obj.stop()
    time.sleep(5)  # Simulate downtime
    print("Kafka container stopped.")

    # Step 3: Restart Kafka container
    print("\nRestarting Kafka container...")
    kafka_container_obj.start()
    print("Kafka container restarted successfully!")

    # Step 4: Consume messages after restart
    print("\nConsuming message from Kafka after restart...")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_container,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=5000
    )

    # Retrieve messages
    messages = [msg.value for msg in consumer]

    # Step 5: Validate message persistence
    assert b"Persistent Message" in messages, "Message was not persisted after Kafka restart"
    print("✅ Message successfully retrieved after restart! Persistence confirmed.")

