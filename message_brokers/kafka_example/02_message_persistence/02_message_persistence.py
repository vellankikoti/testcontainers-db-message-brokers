import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'room_management'

# Function to update room availability
def update_room_availability(producer, room_id, available):
    message = {
        'room_id': room_id,
        'available': available,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Room availability updated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle room management confirmation
def handle_room_management(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        room_update = message.value
        print(f"Received room update: {room_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_room_management(kafka_container):
    # Initialize Kafka Producer and Consumer using the Kafka container's address
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='room_management_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Update room availability
    update_room_availability(producer, room_id=101, available=True)
    update_room_availability(producer, room_id=102, available=False)

    # Start handling room management messages
    print("Listening for room management updates...")
    handle_room_management(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
