"""
07_custom_docker_image.py - Custom Docker Image Example

This example demonstrates using a custom Docker image for RabbitMQ with Testcontainers.
It tests sending messages to a RabbitMQ queue using a custom image.
"""

import pika
import time
from testcontainers.core.container import DockerContainer

def send_message(queue_name, message, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(f"[x] Message sent to {queue_name}: {message}")

    connection.close()

def test_send_custom_message(rabbitmq_container):
    """Test sending a message using a custom Docker image."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send a message using the RabbitMQ container's connection parameters
    queue_name = 'custom_queue'
    message = 'Hello from custom Docker image!'
    send_message(queue_name, message, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=queue_name)

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    expected_message = message
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with DockerContainer("your_custom_rabbitmq_image:latest") as rabbitmq:
        send_message("custom_queue", "Hello from custom Docker image!", rabbitmq.get_connection_params())
