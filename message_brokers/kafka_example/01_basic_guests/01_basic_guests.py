"""
01_basic_guests.py - Basic Guest Registration System

This example demonstrates a basic guest registration system using Kafka and Testcontainers.
It tests the registration of guests by sending messages to a Kafka topic.
"""

from kafka import KafkaProducer, KafkaConsumer
import json
import time

def register_guest(guest_name, guest_email, guest_phone, bootstrap_servers):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    guest_info = {
        'name': guest_name,
        'email': guest_email,
        'phone': guest_phone
    }

    producer.send('guest_registration', guest_info)
    producer.flush()
    print(f"[x] Guest registered successfully: {guest_name}")

def test_register_guest(kafka_container):
    """Test registering a guest."""
    # Wait for Kafka to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Register a guest using the Kafka container's connection parameters
    guest_name = "Alice"
    guest_email = "alice@example.com"
    guest_phone = "123-456-7890"
    register_guest(guest_name, guest_email, guest_phone, kafka_container.get_bootstrap_server())

    # Connect to the Kafka container to verify the message
    consumer = KafkaConsumer(
        'guest_registration',
        bootstrap_servers=kafka_container.get_bootstrap_server(),
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',  # Start reading at the earliest message
        enable_auto_commit=True,        # Automatically commit offsets
        group_id='test-group'           # Consumer group ID
    )

    # Verify the message was sent
    for message in consumer:
        expected_message = {
            'name': guest_name,
            'email': guest_email,
            'phone': guest_phone
        }
        assert message.value == expected_message
        print(f"[x] Received confirmation: {message.value}")
        break  # Exit after receiving the first message

    # Close the consumer after processing
    consumer.close()

if __name__ == "__main__":
    from testcontainers.kafka import KafkaContainer

    # Example usage
    with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
        register_guest("Alice", "alice@example.com", "123-456-7890", kafka.get_bootstrap_server())
