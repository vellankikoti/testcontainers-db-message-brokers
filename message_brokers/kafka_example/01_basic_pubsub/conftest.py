"""
conftest.py - Shared fixture for Kafka Testcontainers.
"""

import pytest
import time
from testcontainers.kafka import KafkaContainer
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.fixture(scope="session")
def kafka_container():
    """Starts a Kafka container for testing with necessary configurations."""
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as kafka:
        kafka.with_env("KAFKA_AUTO_CREATE_TOPICS_ENABLE", "true")
        kafka.with_env("KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR", "1")
        kafka.with_env("KAFKA_LISTENERS", "PLAINTEXT://0.0.0.0:9092")
        kafka.with_env("KAFKA_ADVERTISED_LISTENERS", "PLAINTEXT://localhost:9092")

        kafka.with_exposed_ports(9092)  # Ensure the Kafka port is open
        kafka.with_network_mode("bridge")  # Avoid Docker network issues

        # Explicit wait for Kafka startup logs
        wait_for_logs(kafka, "INFO [KafkaServer id=1] started", timeout=60)

        yield kafka.get_bootstrap_server()
