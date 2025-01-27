"""
02_message_persistence.py - Demonstrates Kafka message persistence with Testcontainers.

This example verifies that Kafka retains messages even after container restarts.

Steps:
1. Start a Kafka container using Testcontainers.
2. Produce a message to a Kafka topic.
3. Stop and restart the Kafka broker (simulate failure and recovery).
4. Consume the message after the restart.
5. Verify message persistence using assertions.
"""

import time
import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError


def wait_for_kafka(bootstrap_server, timeout=30):
    """
    Waits for Kafka to be fully ready before allowing producers and consumers to connect.

    Args:
        bootstrap_server (str): Kafka bootstrap server address.
        timeout (int): Maximum wait time in seconds.

    Returns:
        None
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            producer = KafkaProducer(bootstrap_servers=bootstrap_server)
            producer.close()
            return  # Kafka is ready
        except KafkaError:
            time.sleep(2)  # Retry every 2 seconds


def test_kafka_message_persistence(kafka_container, kafka_bootstrap_server):
    """
    Tests Kafka message persistence across broker restarts.

    Steps:
    - Produces a message to a Kafka topic.
    - Stops Kafka to simulate a failure.
    - Restarts Kafka to simulate recovery.
    - Consumes the message after restart.
    - Asserts that the message is retained.

    Args:
        kafka_container: Kafka container instance from Testcontainers.
        kafka_bootstrap_server (str): Kafka bootstrap server URL.

    Returns:
        None
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
    new_bootstrap_server = kafka_container.get_bootstrap_server()
    wait_for_kafka(new_bootstrap_server)  # Ensure Kafka is fully ready after restart

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
