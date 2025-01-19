import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'performance_testing'

# Function to simulate performance testing
def simulate_performance_test(producer, test_id, duration):
    message = {
        'test_id': test_id,
        'duration': duration,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Performance test initiated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle performance test confirmations
def handle_performance_test_confirmation(consumer, max_messages=5, timeout=10):
    message_count = 0
    start_time = time.time()

    while message_count < max_messages:
        # Poll for messages
        message = consumer.poll(timeout_ms=100)  # Poll with a short timeout
        if message:
            for _, messages in message.items():
                for msg in messages:
                    test_update = msg.value
                    print(f"Received performance test update: {test_update}")
                    message_count += 1
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached, exiting...")
            break

    consumer.close()  # Close the consumer after processing

# Test function to run the example
def test_performance_testing(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='performance_testing_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate performance testing
    simulate_performance_test(producer, test_id=1, duration=60)

    # Start handling performance test confirmation messages
    print("Listening for performance test confirmations...")
    handle_performance_test_confirmation(consumer, max_messages=2, timeout=10)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
