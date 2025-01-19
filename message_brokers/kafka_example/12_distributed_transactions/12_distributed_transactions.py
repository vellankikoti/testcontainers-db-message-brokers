import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'distributed_transactions'

# Function to simulate distributed transactions
def simulate_distributed_transaction(producer, transaction_id, details):
    message = {
        'transaction_id': transaction_id,
        'details': details,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Distributed transaction initiated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle distributed transaction confirmations
def handle_transaction_confirmation(consumer, max_messages=5, timeout=10):
    message_count = 0
    start_time = time.time()

    while message_count < max_messages:
        # Poll for messages
        message = consumer.poll(timeout_ms=100)  # Poll with a short timeout
        if message:
            for _, messages in message.items():
                for msg in messages:
                    transaction_update = msg.value
                    print(f"Received transaction update: {transaction_update}")
                    message_count += 1
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached, exiting...")
            break

    consumer.close()  # Close the consumer after processing

# Test function to run the example
def test_distributed_transactions(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='distributed_transactions_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Simulate distributed transactions
    simulate_distributed_transaction(producer, transaction_id=1, details='Transfer $100 from A to B')
    simulate_distributed_transaction(producer, transaction_id=2, details='Transfer $200 from C to D')

    # Start handling transaction confirmation messages
    print("Listening for transaction confirmations...")
    handle_transaction_confirmation(consumer, max_messages=2, timeout=10)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
