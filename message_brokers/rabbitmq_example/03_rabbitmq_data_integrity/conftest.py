"""
conftest.py - Shared test configuration for RabbitMQ Testcontainers.

This file provides a fixture to start a RabbitMQ container before running tests.
"""

import pytest
from testcontainers.rabbitmq import RabbitMQContainer

@pytest.fixture(scope="session")
def rabbitmq_container():
    """
    Starts a RabbitMQ container for testing and provides the AMQP connection URL.

    This fixture:
    - Uses the latest RabbitMQ Docker image.
    - Automatically starts the RabbitMQ container before tests.
    - Ensures the container is stopped after the test session ends.
    
    Returns:
        str: The RabbitMQ AMQP connection URL (e.g., amqp://user:password@localhost:port).
    """
    with RabbitMQContainer("rabbitmq:latest") as rabbitmq:
        yield rabbitmq.get_connection_url()
