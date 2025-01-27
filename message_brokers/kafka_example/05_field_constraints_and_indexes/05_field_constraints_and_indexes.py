"""
05_kafka_field_constraints.py - Validates Kafka message schema and data integrity with Testcontainers.

This example ensures Kafka maintains:
- Message format validation.
- Schema enforcement using JSON structure.
- No duplicate messages.
- Message ordering preservation.
"""

import time
import json
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


def validate_message_schema(message):
    """
    Validates that the Kafka message follows the predefined schema.

    Args:
        message (dict): Message to be validated.

    Returns:
        bool: True if message adheres to schema, else False.
    """
    schema = {"id": int, "name": str, "email": str}
    return all(key in message and isinstance(message[key], schema[key]) for key in schema)


def test_kafka_field_constraints(kafka_container):
    """
    Test case to validate Kafka field constraints by ensuring:
    - Message schema is enforced.
    - No duplicate messages are processed.
    - Message ordering is preserved.

    Steps:
        1. Start a Kafka container.
        2. Produce multiple valid messages.
        3. Attempt to send an invalid message.
        4. Consume messages and validate:
            - Ordering is maintained.
            - No duplicate messages exist.
            - Schema is correctly enforced.
    """
    topic = "field_constraints_topic"

    # Step 1: Produce valid messages
    print("\nProducing valid messages to Kafka...")
    producer = KafkaProducer(bootstrap_servers=kafka_container)

    messages_sent = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]

    for message in messages_sent:
        assert validate_message_schema(message), "Invalid message detected before sending!"
        producer.send(topic, json.dumps(message).encode("utf-8"))

    producer.flush()
    print("✅ Valid messages successfully produced!")

    # Step 2: Produce an invalid message
    print("\nProducing invalid messages to Kafka...")
    invalid_message = {"id": "wrong_type", "name": "Charlie"}  # Missing email and wrong ID type
    assert not validate_message_schema(invalid_message), "Invalid message should have been rejected!"
    print("❌ Invalid message rejected as expected!")

    # Step 3: Consume messages
    print("\nConsuming messages from Kafka...")
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_container,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=5000
    )

    messages_received = [json.loads(msg.value) for msg in consumer]

    # Step 4: Validate message order and uniqueness
    print("\nValidating message order and uniqueness...")

    # Ensure ordering is maintained
    assert messages_received == messages_sent, "Message order was not preserved!"

    # Ensure no duplicate messages exist
    assert len(messages_received) == len(set(json.dumps(m) for m in messages_received)), "Duplicate messages detected!"

    print("✅ Kafka data integrity validation PASSED! 🎉")
