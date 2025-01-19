import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'failure_simulation'

# Function to simulate a failure
def simulate_failure(producer, failure_id, description):
    message = {
        'failure_id': failure_id,
        'description': description,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Failure simulated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle failure confirmations
def handle_failure_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        failure_update = message.value
        print(f"Received failure update: {failure_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_simulating_failures(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='failure_simulation_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate failures
    simulate_failure(producer, failure_id=1, description='Database connection lost')
    simulate_failure(producer, failure_id=2, description='Service timeout')

    # Start handling failure confirmation messages
    print("Listening for failure confirmations...")
    handle_failure_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
