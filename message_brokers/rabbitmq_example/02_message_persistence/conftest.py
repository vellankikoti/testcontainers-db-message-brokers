"""
conftest.py - Shared test configuration for RabbitMQ Testcontainers.

This file provides a fixture to start a RabbitMQ container before running tests.
"""

import time
import pytest
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="session")
def rabbitmq_bootstrap_server():
    """
    Pytest fixture to start a RabbitMQ container and provide its connection parameters.

    Returns:
        RabbitMqContainer: Running RabbitMQ container instance.
    """
    container = RabbitMqContainer("rabbitmq:3.9-management")
    container.start()
    time.sleep(10)  # Ensure RabbitMQ is fully ready
    yield container
    container.stop()
