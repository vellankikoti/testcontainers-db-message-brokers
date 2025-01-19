import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'multiple_containers'

# Function to simulate multiple container interactions
def simulate_multiple_containers(producer, container_id, action):
    message = {
        'container_id': container_id,
        'action': action,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Action on container initiated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle multiple container confirmations
def handle_multiple_container_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        container_update = message.value
        print(f"Received multiple container update: {container_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_multiple_containers(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='multiple_containers_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate actions on multiple containers
    simulate_multiple_containers(producer, container_id='container_1', action='start')
    simulate_multiple_containers(producer, container_id='container_2', action='stop')

    # Start handling multiple container confirmation messages
    print("Listening for multiple container confirmations...")
    handle_multiple_container_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
