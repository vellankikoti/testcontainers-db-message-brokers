"""
conftest.py - Shared test configuration for Kafka Testcontainers.

This file provides a fixture to start a Kafka container before running tests.
"""

import pytest
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="session")
def kafka_bootstrap_server():
    """
    Pytest fixture to start a Kafka container and provide its bootstrap server.

    Returns:
        str: Kafka bootstrap server URL.
    """
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        yield kafka.get_bootstrap_server()
