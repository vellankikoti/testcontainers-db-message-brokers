"""
conftest.py - Shared test configuration for RabbitMQ Testcontainers.

This file provides a fixture to start a RabbitMQ container before running tests.
"""

import pytest
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="session")
def rabbitmq_bootstrap_server():
    """
    Pytest fixture to start a RabbitMQ container and provide its connection URL.

    Returns:
        str: RabbitMQ connection URL.
    """
    with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
        yield rabbitmq.get_connection_url()
