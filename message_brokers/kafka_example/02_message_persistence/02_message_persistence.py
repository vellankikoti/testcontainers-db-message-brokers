"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.
"""

import time
import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.errors import KafkaError


@pytest.fixture(scope="module")
def kafka_container():
    """
    Starts a Kafka container and ensures it's ready before running tests.
    """
    container = KafkaContainer("confluentinc/cp-kafka:latest")
    container.start()
    wait_for_kafka(container.get_bootstrap_server())  # Ensure Kafka is ready
    yield container
    container.stop()


@pytest.fixture(scope="function")
def kafka_bootstrap_server(kafka_container):
    """
    Provides the Kafka bootstrap server URL for each test function.
    """
    return kafka_container.get_bootstrap_server()


def wait_for_kafka(bootstrap_server, timeout=30):
    """
    Waits for Kafka to be fully ready by using KafkaAdminClient.

    Args:
        bootstrap_server (str): Kafka bootstrap server address.
        timeout (int): Maximum wait time in seconds.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_server)
            admin_client.list_topics()
            admin_client.close()
            return  # Kafka is ready
        except KafkaError:
            time.sleep(2)  # Retry every 2 seconds


def test_kafka_message_persistence(kafka_container, kafka_bootstrap_server):
    """
    Tests Kafka message persistence across broker restarts.

    Steps:
    - Produces a message to a Kafka topic.
    - Restarts Kafka (instead of stopping to ensure persistence).
    - Consumes the message after restart.
    - Asserts that the message is retained.
    """
    topic = "persistent_topic"

    # Step 1: Produce a persistent message
    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_server)
    producer.send(topic, b"Persistent Message")
    producer.flush()
    producer.close()

    # Step 2: Restart Kafka (Instead of stop/start, use Docker restart)
    kafka_container._container.restart()
    time.sleep(5)  # Give Kafka time to restart
    new_bootstrap_server = kafka_container.get_bootstrap_server()
    wait_for_kafka(new_bootstrap_server)  # Ensure Kafka is ready

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
