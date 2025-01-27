"""
conftest.py - Shared Kafka fixture using Testcontainers (NO docker-compose).
"""

import pytest
import time
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from testcontainers.core.container import DockerContainer


@pytest.fixture(scope="session")
def zookeeper_container():
    """Starts Zookeeper using Testcontainers."""
    with DockerContainer("confluentinc/cp-zookeeper:latest").with_env(
        "ZOOKEEPER_CLIENT_PORT", "2181"
    ) as zookeeper:
        zookeeper.start()
        yield zookeeper.get_container_host_ip() + ":2181"


@pytest.fixture(scope="session")
def kafka_container(zookeeper_container):
    """Starts Kafka using Testcontainers."""
    with DockerContainer("confluentinc/cp-kafka:latest") as kafka:
        kafka.with_env("KAFKA_BROKER_ID", "1")
        kafka.with_env("KAFKA_ZOOKEEPER_CONNECT", zookeeper_container)
        kafka.with_env("KAFKA_ADVERTISED_LISTENERS", "PLAINTEXT://localhost:9092")
        kafka.with_env("KAFKA_LISTENERS", "PLAINTEXT://0.0.0.0:9092")
        kafka.with_env("KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR", "1")
        kafka.with_exposed_ports(9092)

        kafka.start()

        # ✅ Wait until Kafka is fully ready
        bootstrap_server = "localhost:9092"
        max_wait_time = 30  # Max wait time in seconds
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            try:
                admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_server)
                topics = admin_client.list_topics()
                if topics is not None:
                    break  # Kafka is ready
            except Exception:
                time.sleep(2)  # Retry every 2 seconds

        yield bootstrap_server


@pytest.fixture
def kafka_producer(kafka_container):
    """Creates a Kafka producer."""
    producer = KafkaProducer(
        bootstrap_servers=kafka_container,
        value_serializer=lambda v: v.encode("utf-8"),
        acks="all",
        retries=5
    )
    yield producer
    producer.close()


@pytest.fixture
def kafka_consumer(kafka_container):
    """Creates a Kafka consumer."""
    consumer = KafkaConsumer(
        "test_topic",
        bootstrap_servers=kafka_container,
        value_deserializer=lambda x: x.decode("utf-8"),
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )
    yield consumer
    consumer.close()
