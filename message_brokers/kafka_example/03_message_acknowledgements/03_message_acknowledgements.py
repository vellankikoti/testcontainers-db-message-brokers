import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'reservations'

# Function to create a reservation
def create_reservation(producer, reservation_id, guest_name):
    message = {
        'reservation_id': reservation_id,
        'guest_name': guest_name,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Reservation created: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle reservation confirmations
def handle_reservation_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        reservation_update = message.value
        print(f"Received reservation update: {reservation_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_reservations(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='reservations_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Create reservations
    create_reservation(producer, reservation_id=1, guest_name='Alice')
    create_reservation(producer, reservation_id=2, guest_name='Bob')

    # Start handling reservation confirmation messages
    print("Listening for reservation confirmations...")
    handle_reservation_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
