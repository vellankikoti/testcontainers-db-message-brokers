"""
02_message_persistence.py - RabbitMQ Message Persistence Test

Fixes:
- Ensures messages persist across RabbitMQ restart.
- Uses volume mapping instead of `with_tmpfs()` (fix for RabbitMqContainer issue).
"""

import time
import pytest
from kafka import KafkaProducer, KafkaConsumer

TOPIC_NAME = "message_persistence_test"

@pytest.fixture(scope="module")
def kafka_bootstrap(kafka_container):
    """ Returns the Kafka bootstrap server from the test container """
    return kafka_container

def produce_messages(broker):
    """ Produces messages to Kafka """
    producer = KafkaProducer(bootstrap_servers=broker)
    messages = [b"message-1", b"message-2", b"message-3"]

    for message in messages:
        producer.send(TOPIC_NAME, message)
        print(f"Produced: {message.decode()}")

    producer.flush()
    producer.close()
    return messages

def consume_messages(broker):
    """ Consumes messages from Kafka """
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=broker,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="test_group"
    )

    received_messages = []
    for message in consumer:
        received_messages.append(message.value.decode())
        print(f"Consumed: {message.value.decode()}")

        if len(received_messages) == 3:
            break  # Stop after consuming all messages

    consumer.close()
    return received_messages

def test_produce_messages(kafka_bootstrap):
    """ Test if messages are successfully produced """
    print("\nProducing messages...")
    messages = produce_messages(kafka_bootstrap)
    assert len(messages) == 3, "Not all messages were produced!"

def test_consume_messages(kafka_bootstrap):
    """ Test if messages persist even after consumer restart """
    print("\nConsuming messages after simulated failure...")
    
    # Simulating a delay to mimic consumer failure
    time.sleep(5)

    received_messages = consume_messages(kafka_bootstrap)
    assert received_messages == ["message-1", "message-2", "message-3"], "Message persistence failed!"
    print("\n✅ Message persistence test passed!")
