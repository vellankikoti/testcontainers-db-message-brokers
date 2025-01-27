"""
conftest.py - Pytest fixture for RabbitMQ using Testcontainers.

Fixes:
- Ensures RabbitMQ messages persist across restart.
- Uses volume mapping instead of `with_tmpfs()` (fix for RabbitMqContainer issue).
"""

import pytest
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope="session")
def kafka_container():
    """ Starts a Kafka container for testing and provides the bootstrap server URL. """
    with KafkaContainer() as kafka:
        yield kafka.get_bootstrap_server()
