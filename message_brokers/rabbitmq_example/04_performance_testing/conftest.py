"""
conftest.py - Shared fixtures for RabbitMQ example
"""

import pytest
from testcontainers.rabbitmq import RabbitMqContainer
import pika

@pytest.fixture(scope="module")
def rabbitmq_container():
    """Start a RabbitMQ container and provide the connection details."""
    with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
        yield rabbitmq

@pytest.fixture(scope="module")
def rabbitmq_connection(rabbitmq_container):
    """Set up a RabbitMQ connection."""
    parameters = pika.ConnectionParameters(host=rabbitmq_container.get_container_host_ip(),
                                           port=rabbitmq_container.get_exposed_port(5672))
    connection = pika.BlockingConnection(parameters)
    yield connection
    connection.close()