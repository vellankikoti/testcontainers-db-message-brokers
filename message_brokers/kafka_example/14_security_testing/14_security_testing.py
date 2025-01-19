import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'security_testing'

# Function to simulate a security test
def simulate_security_test(producer, test_id, description):
    message = {
        'test_id': test_id,
        'description': description,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Security test initiated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle security test confirmations
def handle_security_test_confirmation(consumer, max_messages=5):
    message_count = 0
    for message in consumer:
        test_update = message.value
        print(f"Received security test update: {test_update}")
        message_count += 1
        if message_count >= max_messages:
            break  # Exit after processing a limited number of messages

# Test function to run the example
def test_security_testing(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='security_testing_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate security tests
    simulate_security_test(producer, test_id=1, description='SQL Injection Test')
    simulate_security_test(producer, test_id=2, description='Cross-Site Scripting Test')

    # Start handling security test confirmation messages
    print("Listening for security test confirmations...")
    handle_security_test_confirmation(consumer, max_messages=2)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
