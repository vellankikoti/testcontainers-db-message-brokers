import time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import pytest

KAFKA_TOPIC = 'occupancy_report'

# Function to generate occupancy report
def generate_occupancy_report(producer, report_id, occupancy_data):
    message = {
        'report_id': report_id,
        'occupancy_data': occupancy_data,
        'timestamp': time.time()
    }
    try:
        producer.send(KAFKA_TOPIC, message)
        producer.flush()
        print(f"Occupancy report generated: {message}")
    except KafkaError as e:
        print(f"Error sending message: {e}")

# Function to handle occupancy report confirmations
def handle_occupancy_report_confirmation(consumer, max_messages=5, timeout=10):
    message_count = 0
    start_time = time.time()

    while message_count < max_messages:
        # Poll for messages
        message = consumer.poll(timeout_ms=100)  # Poll with a short timeout
        if message:
            for _, messages in message.items():
                for msg in messages:
                    report_update = msg.value
                    print(f"Received occupancy report update: {report_update}")
                    message_count += 1
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            print("Timeout reached, exiting...")
            break

    consumer.close()  # Close the consumer after processing

# Test function to run the example
def test_occupancy_report(kafka_container):
    producer = KafkaProducer(bootstrap_servers=kafka_container.get_bootstrap_server(),
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=kafka_container.get_bootstrap_server(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='occupancy_report_group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    # Generate occupancy report
    occupancy_data = {'room_101': 'occupied', 'room_102': 'available'}
    generate_occupancy_report(producer, report_id=1, occupancy_data=occupancy_data)

    # Start handling occupancy report confirmation messages
    print("Listening for occupancy report confirmations...")
    handle_occupancy_report_confirmation(consumer, max_messages=2, timeout=10)  # Limit to 2 messages for this example

if __name__ == "__main__":
    pytest.main([__file__])
