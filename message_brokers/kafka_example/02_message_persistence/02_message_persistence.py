"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.
"""

import time
import pytest
import docker
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
        .with_env("KAFKA_ADVERTISED_LISTENERS", "PLAINTEXT://localhost:9092") \
        .with_env("KAFKA_LISTENERS", "PLAINTEXT://0.0.0.0:9092") \
        .with_env("KAFKA_BROKER_ID", "1") \
        .with_env("KAFKA_LOG_DIRS", "/var/lib/kafka/data") \
        .with_volume_mapping("/tmp/kafka-data", "/var/lib/kafka/data") \
        .with_exposed_ports(9092) \
        .with_command(
            "bash -c 'echo Waiting for Kafka... && sleep 30 && /etc/confluent/docker/run'"
        )

    container.start()
    kafka_port = get_kafka_port(container)
    wait_for_kafka(kafka_port)  # Ensure Kafka is fully up
    yield container
    container.stop()


@pytest.fixture(scope="function")
def kafka_bootstrap_server(kafka_container):
    """
    Provides the Kafka bootstrap server URL for each test function.

    Returns:
        str: The Kafka bootstrap server URL.
    """
    return f"localhost:{get_kafka_port(kafka_container)}"


def get_kafka_port(container):
    """
    Retrieves the correct exposed Kafka port from Docker.

    Args:
        container: The running Kafka container.

    Returns:
        int: The mapped Kafka port.
    """
    client = docker.from_env()
    container_info = client.containers.get(container._container.id).attrs
    return container_info["NetworkSettings"]["Ports"]["9092/tcp"][0]["HostPort"]


def wait_for_kafka(port, timeout=90):
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
                print(f"✅ Kafka is ready on localhost:{port}")
                return
        except KafkaError:
            time.sleep(2)  # Retry every 2 seconds
    raise TimeoutError(f"❌ Kafka did not start within {timeout} seconds")


def restart_kafka(container):
    """
    Restarts Kafka within the container without stopping the container itself.

    Args:
        container: The Kafka container instance.

    Returns:
        None
    """
    print("🔄 Restarting Kafka service inside the container...")
    container.exec_run("supervisorctl restart kafka")
    time.sleep(15)  # Give Kafka time to restart
    wait_for_kafka(get_kafka_port(container))  # Ensure Kafka is ready after restart


def test_kafka_message_persistence(kafka_container, kafka_bootstrap_server):
    """
    Tests Kafka message persistence across broker restarts.

    Steps:
    - Produces a message to a Kafka topic.
    - Restarts Kafka within the container.
    - Consumes the message after restart.
    - Asserts that the message is retained.
    """
    topic = "persistent_topic"

    # Step 1: Produce a persistent message
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    producer.send(topic, b"Persistent Message")
    producer.flush()
    producer.close()

    # Step 2: Restart Kafka within the container (preserve logs)
    restart_kafka(kafka_container)

    # Step 3: Consume messages after restart
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_bootstrap_server,
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
