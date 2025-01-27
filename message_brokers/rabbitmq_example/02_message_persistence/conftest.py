"""
conftest.py - Shared test configuration for RabbitMQ Testcontainers.

This file provides a fixture to start a RabbitMQ container before running tests.
"""

import time
import pytest
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.rabbitmq import RabbitMqContainer


@pytest.fixture(scope="session")
def rabbitmq_bootstrap_server():
    """
    Pytest fixture to start a RabbitMQ container and provide its connection parameters.

    Returns:
        RabbitMqContainer: Running RabbitMQ container instance.
    """
    container = RabbitMqContainer("rabbitmq:3.11-management") \
        .with_bind_ports(5672, 5672) \
        .with_bind_ports(15672, 15672)

    container.start()
    wait_for_logs(container, "Server startup complete", timeout=30)
    time.sleep(5)

    yield container
    container.stop()
