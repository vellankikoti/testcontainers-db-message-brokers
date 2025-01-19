"""
conftest.py - Shared fixtures for RabbitMQ examples
"""

import pytest
from testcontainers.rabbitmq import RabbitMqContainer

@pytest.fixture(scope='module')
def rabbitmq_container():
    """Fixture to set up a RabbitMQ container for testing."""
    # Use the custom Docker image
    with RabbitMqContainer("your_custom_rabbitmq_image:latest") as rabbitmq:
        yield rabbitmq
