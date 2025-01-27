"""
02_message_persistence.py - Validates RabbitMQ message persistence with Testcontainers.

This test ensures that RabbitMQ retains messages in a durable queue even after a broker restart.
"""

import time
import pytest
import pika
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="module")
def rabbitmq_container():
    """
    Pytest fixture to start a RabbitMQ container.

    Returns:
        str: RabbitMQ connection URL.
    """
    with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
        yield rabbitmq.get_connection_url()


def test_rabbitmq_message_persistence(rabbitmq_container):
    """
    Test case to validate RabbitMQ message persistence by ensuring:
    - Messages are stored in a durable queue.
    - Messages persist across RabbitMQ restarts.

    Steps:
        1. Start a RabbitMQ container.
        2. Publish persistent messages to a durable queue.
        3. Stop and restart RabbitMQ.
        4. Consume messages and validate:
            - Persistence is maintained across broker restarts.
    """
    queue_name = "persistent_queue"

    # Step 1: Publish messages to RabbitMQ before restart
    print("\nPublishing persistent messages to RabbitMQ...")

    # Establish connection
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_container))
    channel = connection.channel()

    # Declare a durable queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish persistent messages
    persistent_message = "Persistent Message"
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=persistent_message,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )
    connection.close()
    print("✅ Message successfully published!")

    # Step 2: Stop and restart RabbitMQ
    print("\nStopping RabbitMQ container...")
    rabbitmq_container_obj = RabbitMqContainer("rabbitmq:3.9-management")
    rabbitmq_container_obj.stop()
    time.sleep(5)  # Simulate downtime
    print("RabbitMQ container stopped.")

    print("\nRestarting RabbitMQ container...")
    rabbitmq_container_obj.start()
    print("RabbitMQ container restarted successfully!")

    # Step 3: Consume messages after restart
    print("\nConsuming messages from RabbitMQ after restart...")
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_container))
    channel = connection.channel()

    # Declare the durable queue again
    channel.queue_declare(queue=queue_name, durable=True)

    # Retrieve the persisted message
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    connection.close()

    # Step 4: Validate message persistence
    assert body == persistent_message.encode(), "Message was not persisted after RabbitMQ restart!"
    print("✅ Message successfully retrieved after restart! Persistence confirmed.")
