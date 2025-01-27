"""
conftest.py - Pytest fixture setup for Kafka testing with Testcontainers.

This file provides reusable pytest fixtures for managing Kafka containers.
"""

import pytest
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="session")
def kafka_container():
    """
    Starts a Kafka container once per test session.
    This avoids restarting the container multiple times, making tests faster.

    Returns:
        KafkaContainer: A running Kafka container instance.
    """
    container = KafkaContainer("confluentinc/cp-kafka:latest")
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="function")
def kafka_bootstrap_server(kafka_container):
    """
    Provides the Kafka bootstrap server URL for each test function.

    Args:
        kafka_container: The running Kafka container instance.

    Returns:
        str: The Kafka bootstrap server URL.
    """
    return kafka_container.get_bootstrap_server()
