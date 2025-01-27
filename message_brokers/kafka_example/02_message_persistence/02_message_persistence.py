"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.
"""

import time
import pytest
from testcontainers.core.container import DockerContainer
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.errors import KafkaError


@pytest.fixture(scope="module")
def kafka_container():
    """
    Starts a Kafka container with persistent storage for message retention.

    Returns:
        DockerContainer: A running Kafka container instance.
    """
    container = DockerContainer("confluentinc/cp-kafka:latest") \
        .with_env("KAFKA_AUTO_CREATE_TOPICS_ENABLE", "true") \
        .with_env("KAFKA_BROKER_ID", "1") \
        .with_env("KAFKA_LOG_DIRS", "/var/lib/kafka/data") \
        .with_volume_mapping("/tmp/kafka-data", "/var/lib/kafka/data") \
        .with_exposed_ports(9092) \
        .with_command(
            "bash -c 'echo Waiting for Kafka... && sleep 20 && /etc/confluent/docker/run'"
        )

    container.start()
    wait_for_kafka(container.get_exposed_port(9092))  # Ensure Kafka is fully up
    yield container
    container.stop()


@pytest.fixture(scope="function")
def kafka_bootstrap_server(kafka_container):
    """
    Provides the Kafka bootstrap server URL for each test function.

    Returns:
        str: The Kafka bootstrap server URL.
    """
    return f"localhost:{kafka_container.get_exposed_port(9092)}"


def wait_for_kafka(port, timeout=40):
    """
    Waits for Kafka to be fully ready before allowing producers and consumers to connect.

    Args:
        port (int): Kafka broker port.
        timeout (int): Maximum wait time in seconds.

    Returns:
        None
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=f"localhost:{port}")
            topics = admin_client.list_topics()
            admin_client.close()
            if topics:  # Ensure Kafka is actually working
                return
        except KafkaError:
            time.sleep(2)  # Retry every 2 seconds


def test_kafka_message_persistence(kafka_container, kafka_bootstrap_server):
    """
    Tests Kafka message persistence across broker restarts.

    Steps:
    - Produces a message to a Kafka topic.
    - Restarts Kafka container.
    - Consumes the message after restart.
    - Asserts that the message is retained.
    """
    topic = "persistent_topic"

    # Step 1: Produce a persistent message
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    producer.send(topic, b"Persistent Message")
    producer.flush()
    producer.close()

    # Step 2: Restart Kafka using Docker restart (not stop/start)
    kafka_container._container.restart()
    time.sleep(15)  # Give Kafka time to restart
    new_bootstrap_server = f"localhost:{kafka_container.get_exposed_port(9092)}"
    wait_for_kafka(kafka_container.get_exposed_port(9092))  # Ensure Kafka is fully ready

    # Step 3: Consume messages after restart
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

    # Step 4: Validate message persistence
    assert received_message == b"Persistent Message"
