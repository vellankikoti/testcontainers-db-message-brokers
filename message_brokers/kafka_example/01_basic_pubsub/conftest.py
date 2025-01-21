"""
conftest.py - Shared fixtures for Kafka examples
"""

import pytest
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope='module')
def kafka_container():
    """Fixture to set up a Kafka container for testing."""
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka
