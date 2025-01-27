"""
conftest.py - Shared fixtures for RabbitMQ example using Testcontainers.

This file provides:
1. A fixture to start a RabbitMQ container.
2. A fixture to establish a RabbitMQ connection.
"""

import pytest
from testcontainers.rabbitmq import RabbitMqContainer
import pika

@pytest.fixture(scope="module")
def rabbitmq_container():
    """
    Starts a RabbitMQ container for testing.

    - Uses the RabbitMQ 3.9 Management Docker image.
    - Exposes default RabbitMQ ports for testing.
    - Ensures the container is properly cleaned up after tests.

    Returns:
        RabbitMqContainer: The running RabbitMQ Testcontainer instance.
    """
    with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
        yield rabbitmq

@pytest.fixture(scope="module")
def rabbitmq_connection(rabbitmq_container):
    """
    Establishes a connection to the RabbitMQ container.

    - Retrieves the container's IP and exposed port.
    - Creates a blocking connection using `pika`.
    - Closes the connection automatically after tests.

    Returns:
        pika.BlockingConnection: An active RabbitMQ connection instance.
    """
    parameters = pika.ConnectionParameters(
        host=rabbitmq_container.get_container_host_ip(),
        port=rabbitmq_container.get_exposed_port(5672)
    )
    connection = pika.BlockingConnection(parameters)
    yield connection
    connection.close()
