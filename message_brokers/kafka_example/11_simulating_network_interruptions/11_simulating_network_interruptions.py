import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'network_interruptions'

# Function to simulate network interruptions
def simulate_network_interruption(producer, interruption_id, description):
    message = {
        'interruption_id': interruption_id,
        'description': description,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Network interruption simulated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle network interruption confirmations
def handle_network_interruption_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        interruption_update = message.value
        print(f"Received network interruption update: {interruption_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_simulating_network_interruptions(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='network_interruptions_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate network interruptions
    simulate_network_interruption(producer, interruption_id=1, description='Connection timeout')
    simulate_network_interruption(producer, interruption_id=2, description='Packet loss')

    # Start handling network interruption confirmation messages
    print("Listening for network interruption confirmations...")
    handle_network_interruption_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
