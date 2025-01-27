"""
conftest.py - Shared test configuration for RabbitMQ Testcontainers.

This file provides a fixture to start a RabbitMQ container before running tests.
"""

import pytest
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="session")
def rabbitmq_bootstrap_server():
    """
    Pytest fixture to start a RabbitMQ container and provide its connection parameters.

    Returns:
        dict: RabbitMQ connection parameters.
    """
    with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
        rabbitmq.start()
        yield {
            "container": rabbitmq,
            "host": rabbitmq.get_connection_params()["host"],
            "port": rabbitmq.get_connection_params()["port"],
            "username": rabbitmq.get_connection_params()["username"],
            "password": rabbitmq.get_connection_params()["password"]
        }
