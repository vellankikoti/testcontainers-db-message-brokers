"""
08_performance_testing.py - Performance Testing

This example demonstrates performance testing of message sending using RabbitMQ and Testcontainers.
It tests the speed of sending messages to a RabbitMQ queue.
"""

import pika
import time

def send_performance_messages(num_messages, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='performance_test')

    start_time = time.time()
    for i in range(num_messages):
        message = f"Performance message {i+1}"
        channel.basic_publish(exchange='', routing_key='performance_test', body=message)

    end_time = time.time()
    print(f"[x] Sent {num_messages} messages in {end_time - start_time:.2f} seconds")

    connection.close()

def test_send_performance_messages(rabbitmq_container):
    """Test sending performance messages."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send performance messages using the RabbitMQ container's connection parameters
    num_messages = 1000
    send_performance_messages(num_messages, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the messages were sent
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='performance_test')

    # Verify the number of messages sent
    message_count = channel.queue_declare(queue='performance_test', passive=True).method.message_count
    assert message_count == num_messages

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        send_performance_messages(1000, rabbitmq.get_connection_params())
