"""
conftest.py - Shared fixtures for RabbitMQ examples
"""

import pytest
from testcontainers.rabbitmq import RabbitMqContainer

@pytest.fixture(scope='module')
def rabbitmq_container():
    """Fixture to set up a RabbitMQ container for testing."""
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        yield rabbitmq
