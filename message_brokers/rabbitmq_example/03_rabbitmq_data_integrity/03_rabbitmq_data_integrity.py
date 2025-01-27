"""
03_rabbitmq_data_integrity.py - RabbitMQ Data Integrity Test with Testcontainers.

This test verifies:
1. Message Order: Ensures messages are received in the correct order.
2. Message Uniqueness: Detects and prevents duplicate messages.
3. Message Completeness: Ensures all published messages are consumed.

The test uses Testcontainers to spin up a RabbitMQ instance in Docker.
"""

import time
import pytest
import pika

# Define the queue name for the test
QUEUE_NAME = "data_integrity_queue"

@pytest.fixture(scope="module")
def rabbitmq_url(rabbitmq_container):
    """
    Provides the RabbitMQ connection URL from the Testcontainers instance.

    This fixture:
    - Retrieves the connection string from the running RabbitMQ container.
    - Ensures RabbitMQ is available before the test begins.
    
    Returns:
        str: The RabbitMQ AMQP connection URL.
    """
    return rabbitmq_container

def publish_messages(rabbitmq_url):
    """
    Publishes a sequence of messages to RabbitMQ.

    Args:
        rabbitmq_url (str): The RabbitMQ connection URL.

    Returns:
        list: A list of sent messages.
    """
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    
    # Ensure the queue is declared before publishing messages
    channel.queue_declare(queue=QUEUE_NAME)

    messages = ["Message 1", "Message 2", "Message 3"]
    
    for msg in messages:
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=msg)
        print(f"Produced: {msg}")

    connection.close()
    return messages

def consume_messages(rabbitmq_url):
    """
    Consumes messages from RabbitMQ and validates their order.

    Args:
        rabbitmq_url (str): The RabbitMQ connection URL.

    Returns:
        list: A list of received messages.
    """
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    received_messages = []

    for method_frame, properties, body in channel.consume(QUEUE_NAME, auto_ack=True):
        received_messages.append(body.decode())
        print(f"Consumed: {body.decode()}")

        # Stop consuming after retrieving all expected messages
        if len(received_messages) == 3:
            break

    connection.close()
    return received_messages

def test_data_integrity(rabbitmq_url):
    """
    Tests RabbitMQ message integrity by checking:
    - Message order is preserved.
    - No duplicate messages exist.
    - All messages are received.

    Args:
        rabbitmq_url (str): The RabbitMQ connection URL.
    """
    print("\nProducing messages...")
    sent_messages = publish_messages(rabbitmq_url)
    
    print("\nSimulating delay before consuming messages...")
    time.sleep(5)  # Simulates real-world delay in message processing

    print("\nConsuming messages...")
    received_messages = consume_messages(rabbitmq_url)

    # ✅ Check message order integrity
    assert received_messages == sent_messages, "⚠️ Message order was not preserved!"

    # ✅ Check for duplicate messages
    assert len(received_messages) == len(set(received_messages)), "⚠️ Duplicate messages detected!"

    # ✅ Check message completeness
    assert set(received_messages) == set(sent_messages), "⚠️ Some messages are missing!"

    print("\n✅ RabbitMQ Data Integrity Test Passed!")
