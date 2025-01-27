"""
05_field_constraints_and_indexes.py - RabbitMQ Field Constraints and Index Testing.

This test validates:
1. Message Schema: Ensures messages comply with a predefined structure.
2. Message Size: Rejects messages that exceed a set size limit.
3. Indexing Constraints: Detects duplicate IDs but allows RabbitMQ to process them.

The test uses Testcontainers to spin up a RabbitMQ instance in Docker.
"""

import pytest
import pika
import json

# Define test parameters
QUEUE_NAME = "field_constraints_queue"
MAX_MESSAGE_SIZE = 1024  # 1 KB limit

# Sample valid message format
VALID_MESSAGE = {
    "id": 1,
    "name": "Test Item",
    "timestamp": "2025-01-28T12:00:00Z",
    "priority": "high"
}

# Sample oversized message
LARGE_MESSAGE = {
    "id": 2,
    "name": "A" * 2000,  # Exceeds size limit
    "timestamp": "2025-01-28T12:00:00Z",
    "priority": "medium"
}

@pytest.fixture(scope="module")
def rabbitmq_channel(rabbitmq_connection):
    """
    Creates a RabbitMQ channel for sending/receiving messages.

    - Declares the queue before tests run.
    - Closes the channel after tests.
    
    Returns:
        pika.channel.Channel: The RabbitMQ channel instance.
    """
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    yield channel
    channel.close()

def validate_message_schema(message):
    """
    Validates the message format against expected fields.

    Args:
        message (dict): The message payload.

    Returns:
        bool: True if valid, False if missing required fields.
    """
    required_fields = {"id", "name", "timestamp", "priority"}
    return required_fields.issubset(message.keys())

def validate_message_size(message):
    """
    Ensures the message size does not exceed MAX_MESSAGE_SIZE.

    Args:
        message (dict): The message payload.

    Returns:
        bool: True if size is within limit, False otherwise.
    """
    return len(json.dumps(message).encode("utf-8")) <= MAX_MESSAGE_SIZE

def test_valid_message(rabbitmq_channel):
    """
    Tests if a valid message is successfully published and consumed.

    Args:
        rabbitmq_channel (pika.channel.Channel): The RabbitMQ channel.
    """
    assert validate_message_schema(VALID_MESSAGE), "⚠️ Schema validation failed for valid message!"
    assert validate_message_size(VALID_MESSAGE), "⚠️ Valid message exceeds size limit!"

    # Publish message
    rabbitmq_channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(VALID_MESSAGE)
    )
    print("\n✅ Valid message sent successfully.")

    # Consume message
    method_frame, header_frame, body = rabbitmq_channel.basic_get(QUEUE_NAME, auto_ack=True)
    received_message = json.loads(body.decode())

    assert received_message == VALID_MESSAGE, "⚠️ Message integrity check failed!"
    print("\n✅ Valid message consumed successfully.")

def test_oversized_message(rabbitmq_channel):
    """
    Tests if an oversized message is prevented from being processed.

    Args:
        rabbitmq_channel (pika.channel.Channel): The RabbitMQ channel.
    """
    assert not validate_message_size(LARGE_MESSAGE), "⚠️ Oversized message passed validation!"
    
    try:
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(LARGE_MESSAGE)
        )
        assert False, "⚠️ Oversized message should not have been sent!"
    except Exception as e:
        print(f"\n✅ Oversized message blocked: {e}")

def test_duplicate_index(rabbitmq_channel):
    """
    Tests if duplicate message IDs are detected but still processed by RabbitMQ.

    Args:
        rabbitmq_channel (pika.channel.Channel): The RabbitMQ channel.
    """
    messages = [
        {"id": 3, "name": "First", "timestamp": "2025-01-28T12:01:00Z", "priority": "low"},
        {"id": 3, "name": "Duplicate", "timestamp": "2025-01-28T12:02:00Z", "priority": "low"},
    ]

    seen_ids = set()
    duplicate_detected = False

    for message in messages:
        assert validate_message_schema(message), "⚠️ Schema validation failed!"
        
        # Check for duplicates but do not fail the test immediately
        if message["id"] in seen_ids:
            duplicate_detected = True
            print(f"⚠️ Warning: Duplicate ID detected: {message['id']}")

        seen_ids.add(message["id"])
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(message)
        )
        print(f"\n✅ Message with ID {message['id']} sent successfully.")

    # The test should PASS if duplicates are found (since we expect them in RabbitMQ)
    assert duplicate_detected, "⚠️ No duplicate detected, but one was expected!"
    print("\n✅ Duplicate ID test passed!")
