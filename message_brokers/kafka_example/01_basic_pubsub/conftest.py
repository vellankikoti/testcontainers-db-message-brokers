"""
conftest.py - Shared Kafka fixture using Testcontainers.
"""

import pytest
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="session")
def kafka_container():
    """
    Starts a Kafka container once per test session.
    This avoids restarting the container multiple times, making tests faster.
    """
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka


@pytest.fixture(scope="function")
def kafka_bootstrap_server(kafka_container):
    """
    Provides the Kafka bootstrap server URL for each test function.
    Ensures a fresh session without restarting the container.
    """
    return kafka_container.get_bootstrap_server()

    
