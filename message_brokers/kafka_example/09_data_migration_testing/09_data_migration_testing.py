import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'data_migration_testing'

# Function to simulate data migration
def simulate_data_migration(producer, migration_id, source, destination):
    message = {
        'migration_id': migration_id,
        'source': source,
        'destination': destination,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Data migration initiated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle data migration confirmations
def handle_data_migration_confirmation(consumer, max_messages=5, timeout=10):
    message_count = 0
    start_time = time.time()

    while message_count < max_messages:
        # Poll for messages
        message = consumer.poll(timeout_ms=100)  # Poll with a short timeout
        if message:
            for _, messages in message.items():
                for msg in messages:
                    migration_update = msg.value
                    print(f"Received data migration update: {migration_update}")
                    message_count += 1
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached, exiting...")
            break

    consumer.close()  # Close the consumer after processing

# Test function to run the example
def test_data_migration_testing(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='data_migration_testing_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate data migration
    simulate_data_migration(producer, migration_id=1, source='db_old', destination='db_new')

    # Start handling data migration confirmation messages
    print("Listening for data migration confirmations...")
    handle_data_migration_confirmation(consumer, max_messages=2, timeout=10)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
