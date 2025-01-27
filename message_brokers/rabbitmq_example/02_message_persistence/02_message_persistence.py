"""
02_message_persistence.py - Validates RabbitMQ message persistence with Testcontainers.

This test ensures that RabbitMQ retains messages in a durable queue even after a broker restart.
"""

import time
import pytest
import pika
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="module")
def rabbitmq_container():
    """
    Pytest fixture to start a RabbitMQ container with persistent storage.

    Returns:
        RabbitMqContainer: Running RabbitMQ container instance.
    """
    container = RabbitMqContainer("rabbitmq:3.11-management") \
        .with_bind_ports(5672, 5672) \
        .with_bind_ports(15672, 15672) \
        .with_volume_mapping("/tmp/rabbitmq-data", "/var/lib/rabbitmq", mode="rw")  # Persistent storage

    container.start()

    # Wait for RabbitMQ to fully start
    wait_for_logs(container, "Server startup complete", timeout=30)
    time.sleep(5)

    yield container

    container.stop()


def get_rabbitmq_connection(container):
    """
    Establish a connection to RabbitMQ using `pika`.

    Args:
        container (RabbitMqContainer): Running RabbitMQ container.

    Returns:
        pika.BlockingConnection: Connection to RabbitMQ.
    """
    credentials = pika.PlainCredentials("guest", "guest")

    connection_params = pika.ConnectionParameters(
        host=container.get_container_host_ip(),
        port=int(container.get_exposed_port(5672)),
        virtual_host="/",
        credentials=credentials,
        heartbeat=600,  # Prevents premature disconnects
        blocked_connection_timeout=300,
    )
    return pika.BlockingConnection(connection_params)


def test_rabbitmq_message_persistence(rabbitmq_container):
    """
    Test case to validate RabbitMQ message persistence by ensuring:
    - Messages are stored in a durable queue.
    - Messages persist across RabbitMQ restarts.

    Steps:
        1. Start a RabbitMQ container with persistent storage.
        2. Publish persistent messages to a durable queue.
        3. Stop and restart RabbitMQ.
        4. Consume messages and validate:
            - Persistence is maintained across broker restarts.
    """
    queue_name = "persistent_queue"

    # Step 1: Publish messages to RabbitMQ before restart
    print("\nPublishing persistent messages to RabbitMQ...")

    connection = get_rabbitmq_connection(rabbitmq_container)
    channel = connection.channel()

    # Declare a durable queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish persistent messages
    persistent_message = "Persistent Message"
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=persistent_message,
        properties=pika.BasicProperties(delivery_mode=2),  # Persistent message
    )
    connection.close()
    print("✅ Message successfully published!")

    # Step 2: Stop and restart RabbitMQ
    print("\nStopping RabbitMQ container...")
    rabbitmq_container.stop()
    time.sleep(5)  # Simulate downtime
    print("RabbitMQ container stopped.")

    print("\nRestarting RabbitMQ container...")
    rabbitmq_container.start()
    wait_for_logs(rabbitmq_container, "Server startup complete", timeout=30)
    time.sleep(5)  # Ensure RabbitMQ is up
    print("RabbitMQ container restarted successfully!")

    # Step 3: Consume messages after restart
    print("\nConsuming messages from RabbitMQ after restart...")
    connection = get_rabbitmq_connection(rabbitmq_container)
    channel = connection.channel()

    # Declare the durable queue again
    channel.queue_declare(queue=queue_name, durable=True)

    # Retrieve the persisted message
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)

    connection.close()

    # Step 4: Validate message persistence
    assert body == persistent_message.encode(), "❌ Message was not persisted after RabbitMQ restart!"
    print("✅ Message successfully retrieved after restart! Persistence confirmed.")
