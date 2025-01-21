import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'extended_stays'

# Function to extend a stay
def extend_stay(producer, stay_id, additional_days):
    message = {
        'stay_id': stay_id,
        'additional_days': additional_days,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Stay extended: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle stay extension confirmations
def handle_stay_extension_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        stay_update = message.value
        print(f"Received stay extension update: {stay_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_extended_stays(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='extended_stays_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Extend stays
    extend_stay(producer, stay_id=1, additional_days=3)
    extend_stay(producer, stay_id=2, additional_days=5)

    # Start handling stay extension confirmation messages
    print("Listening for stay extension confirmations...")
    handle_stay_extension_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
