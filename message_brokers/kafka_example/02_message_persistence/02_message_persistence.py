"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.
"""
import time
import pytest
from testcontainers.core.container import DockerContainer
from kafka import KafkaProducer, KafkaConsumer


@pytest.fixture(scope="module")
def kafka_container():
    """
    Starts a Kafka container with a persistent volume.
    This ensures that messages persist across restarts.
    """
    container = DockerContainer("confluentinc/cp-kafka:latest") \
        .with_env("KAFKA_AUTO_CREATE_TOPICS_ENABLE", "true") \
        .with_env("KAFKA_BROKER_ID", "1") \
        .with_env("KAFKA_LOG_DIRS", "/var/lib/kafka/data") \
        .with_volume_mapping("/tmp/kafka-data", "/var/lib/kafka/data") \
        .with_exposed_ports(9092, 9093) \
        .with_command(
            "bash -c 'echo Waiting for Kafka to be ready... && sleep 10 && /etc/confluent/docker/run'"
        )

    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="function")
def kafka_bootstrap_server(kafka_container):
    """
    Provides the Kafka bootstrap server URL for each test function.
    """
    return f"localhost:{kafka_container.get_exposed_port(9092)}"


def test_kafka_message_persistence(kafka_container, kafka_bootstrap_server):
    """
    Tests Kafka message persistence across broker restarts.
    """
    topic = "persistent_topic"

    # Step 1: Produce a persistent message
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    producer.send(topic, b"Persistent Message")
    producer.flush()
    producer.close()

    # Step 2: Stop Kafka (Simulate broker failure)
    kafka_container.stop()
    time.sleep(5)  # Simulate downtime

    # Step 3: Restart Kafka (Simulate recovery)
    kafka_container.start()
    new_bootstrap_server = f"localhost:{kafka_container.get_exposed_port(9092)}"

    # Step 4: Consume messages after restart
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=new_bootstrap_server,
        auto_offset_reset="earliest",
        group_id="persistence-test-group",
        enable_auto_commit=True,
    )

    received_message = None
    for _ in range(10):  # Retry polling for 10 seconds
        for message in consumer:
            received_message = message.value
            break
        if received_message:
            break
        time.sleep(1)

    consumer.close()

    # Step 5: Validate message persistence
    assert received_message == b"Persistent Message"
