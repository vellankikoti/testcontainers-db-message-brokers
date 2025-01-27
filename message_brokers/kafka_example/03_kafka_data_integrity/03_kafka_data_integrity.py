"""
03_kafka_data_integrity.py - Validates Kafka message integrity with Testcontainers.

This example ensures Kafka maintains:
- Message order integrity.
- No duplicate messages.
- Accurate data retrieval upon consumption.
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
        str: Kafka bootstrap server URL.
    """
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka.get_bootstrap_server()


def test_kafka_data_integrity(kafka_container):
    """
    Test case to validate Kafka data integrity by ensuring:
    - Message ordering is maintained.
    - No duplicate messages.
    - Correct data retrieval after message consumption.

    Steps:
        1. Start a Kafka container.
        2. Produce multiple messages to a Kafka topic.
        3. Consume messages and validate:
            - Ordering of messages is maintained.
            - No messages are duplicated.
            - All messages are correctly received.
    """
    topic = "data_integrity_topic"

    # Step 1: Produce messages
    print("\nProducing messages to Kafka...")
    producer = KafkaProducer(bootstrap_servers=kafka_container)

    messages_sent = [b"Message 1", b"Message 2", b"Message 3"]
    
    for message in messages_sent:
        producer.send(topic, message)
    
    producer.flush()
    print("✅ Messages successfully produced!")

    # Step 2: Consume messages
    print("\nConsuming messages from Kafka...")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_container,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=5000
    )

    messages_received = [msg.value for msg in consumer]

    # Step 3: Validate data integrity
    print("\nValidating message integrity...")

    # Ensure ordering is maintained
    assert messages_received == messages_sent, "Message order was not preserved!"

    # Ensure no duplicates
    assert len(messages_received) == len(set(messages_received)), "Duplicate messages detected!"

    # Ensure all messages were received correctly
    assert set(messages_received) == set(messages_sent), "Some messages are missing!"

    print("✅ Kafka data integrity validation PASSED! 🎉")


