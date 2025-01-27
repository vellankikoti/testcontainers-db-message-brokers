"""
conftest.py - Shared fixture for Kafka Testcontainers.
"""

import pytest
import time
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.kafka import KafkaContainer


@pytest.fixture(scope="session")
def kafka_container():
    """Starts a Kafka container for testing with correct environment variables."""
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as kafka:
        kafka.with_env("KAFKA_AUTO_CREATE_TOPICS_ENABLE", "false")
        kafka.with_env("KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR", "1")

        # Wait for Kafka to be fully ready
        wait_for_logs(kafka, "started (kafka.server.KafkaServer)", timeout=30)

        yield kafka.get_bootstrap_server()
