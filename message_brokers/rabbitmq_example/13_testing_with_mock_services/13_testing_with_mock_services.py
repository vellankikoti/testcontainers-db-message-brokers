"""
13_testing_with_mock_services.py - Testing with Mock Services

This example demonstrates testing with mock services using RabbitMQ and Testcontainers.
It tests sending messages to a mock service queue.
"""

import pika
import time

def send_to_mock_service(service_name, message, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='mock_service')

    full_message = f"{service_name}: {message}"
    channel.basic_publish(exchange='', routing_key='mock_service', body=full_message)
    print(f"[x] Sent to mock service: {full_message}")

    connection.close()

def test_send_to_mock_service(rabbitmq_container):
    """Test sending a message to a mock service."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send a message to a mock service using the RabbitMQ container's connection parameters
    service_name = "UserService"
    message = "Create new user"
    send_to_mock_service(service_name, message, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='mock_service')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='mock_service', auto_ack=True)
    expected_message = f"{service_name}: {message}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        send_to_mock_service("UserService", "Create new user", rabbitmq.get_connection_params())
