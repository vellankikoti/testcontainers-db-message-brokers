import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'mock_services'

# Function to simulate a request to a mock service
def request_mock_service(producer, request_id, service_name):
    message = {
        'request_id': request_id,
        'service_name': service_name,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Request to mock service initiated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle mock service confirmations
def handle_mock_service_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        service_update = message.value
        print(f"Received mock service update: {service_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_testing_with_mock_services(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='mock_services_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Request mock services
    request_mock_service(producer, request_id=1, service_name='User Service')
    request_mock_service(producer, request_id=2, service_name='Payment Service')

    # Start handling mock service confirmation messages
    print("Listening for mock service confirmations...")
    handle_mock_service_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
