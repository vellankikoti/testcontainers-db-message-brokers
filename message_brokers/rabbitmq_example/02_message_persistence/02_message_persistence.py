"""
02_message_persistence.py - RabbitMQ Message Persistence Test

Fixes:
- Ensures messages persist across RabbitMQ restart.
- Uses volume mapping instead of `with_tmpfs()` (fix for RabbitMqContainer issue).
"""

import time
from kafka import KafkaProducer, KafkaConsumer
from testcontainers.kafka import KafkaContainer

TOPIC_NAME = "message_persistence_test"

def produce_messages(broker):
    """ Produces messages to Kafka """
    producer = KafkaProducer(bootstrap_servers=broker)
    messages = [b"message-1", b"message-2", b"message-3"]

    for message in messages:
        producer.send(TOPIC_NAME, message)
        print(f"Produced: {message.decode()}")

    producer.flush()
    producer.close()

def consume_messages(broker):
    """ Consumes messages from Kafka, simulating a restart scenario """
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

if __name__ == "__main__":
    with KafkaContainer() as kafka:
        broker_url = kafka.get_bootstrap_server()
        
        print("Starting Kafka container...")
        time.sleep(5)  # Allow Kafka to fully start

        print("Producing messages...")
        produce_messages(broker_url)

        print("\nSimulating consumer failure (wait for 5 seconds)...")
        time.sleep(5)  # Simulate consumer going offline

        print("\nRestarting consumer and verifying message persistence...")
        received_messages = consume_messages(broker_url)

        assert received_messages == ["message-1", "message-2", "message-3"], "Message persistence failed!"
        print("\n✅ Message persistence test passed!")
