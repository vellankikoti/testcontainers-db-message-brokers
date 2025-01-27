"""
03_rabbitmq_data_integrity.py - RabbitMQ Data Integrity Test using Testcontainers.

This test verifies:
1. Message Order: Ensures messages are received in the correct order.
2. Message Uniqueness: Detects and prevents duplicate messages.
3. Message Completeness: Ensures all published messages are consumed.

The test uses Testcontainers to spin up a RabbitMQ instance in Docker.
"""

import time
import pytest
import pika

# Define the queue name for testing
QUEUE_NAME = "data_integrity_queue"

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

def publish_messages(channel):
    """
    Publishes a sequence of messages to RabbitMQ.

    Args:
        channel (pika.channel.Channel): The RabbitMQ channel.

    Returns:
        list: A list of sent messages.
    """
    messages = ["Message 1", "Message 2", "Message 3"]

    for msg in messages:
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=msg)
        print(f"Produced: {msg}")

    return messages

def consume_messages(channel):
    """
    Consumes messages from RabbitMQ and validates their order.

    Args:
        channel (pika.channel.Channel): The RabbitMQ channel.

    Returns:
        list: A list of received messages.
    """
    received_messages = []

    for method_frame, properties, body in channel.consume(QUEUE_NAME, auto_ack=True):
        received_messages.append(body.decode())
        print(f"Consumed: {body.decode()}")

        if len(received_messages) == 3:
            break  # Stop consuming after retrieving all expected messages

    return received_messages

def test_data_integrity(rabbitmq_channel):
    """
    Tests RabbitMQ message integrity by checking:
    - Message order is preserved.
    - No duplicate messages exist.
    - All messages are received.

    Args:
        rabbitmq_channel (pika.channel.Channel): The RabbitMQ channel.
    """
    print("\nProducing messages...")
    sent_messages = publish_messages(rabbitmq_channel)

    print("\nSimulating delay before consuming messages...")
    time.sleep(5)  # Simulates real-world delay in message processing

    print("\nConsuming messages...")
    received_messages = consume_messages(rabbitmq_channel)

    # ✅ Check message order integrity
    assert received_messages == sent_messages, "⚠️ Message order was not preserved!"

    # ✅ Check for duplicate messages
    assert len(received_messages) == len(set(received_messages)), "⚠️ Duplicate messages detected!"

    # ✅ Check message completeness
    assert set(received_messages) == set(sent_messages), "⚠️ Some messages are missing!"

    print("\n✅ RabbitMQ Data Integrity Test Passed!")
