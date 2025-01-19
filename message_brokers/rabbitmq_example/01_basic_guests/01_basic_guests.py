"""
01_basic_guests.py - Basic Guest Registration System

This example demonstrates a basic guest registration system using RabbitMQ and Testcontainers.
It tests the registration of guests by sending messages to a RabbitMQ queue.
"""

import pika
import time

def register_guest(guest_name, guest_email, guest_phone, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='guest_registration')

    message = f"New guest registered: Name: {guest_name}, Email: {guest_email}, Phone: {guest_phone}"
    channel.basic_publish(exchange='', routing_key='guest_registration', body=message)
    print(f"[x] Guest registered successfully: {guest_name}")

    connection.close()

def test_register_guest(rabbitmq_container):
    """Test registering a guest."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Register a guest using the RabbitMQ container's connection parameters
    guest_name = "Alice"
    guest_email = "alice@example.com"
    guest_phone = "123-456-7890"
    register_guest(guest_name, guest_email, guest_phone, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='guest_registration')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='guest_registration', auto_ack=True)
    expected_message = f"New guest registered: Name: {guest_name}, Email: {guest_email}, Phone: {guest_phone}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        register_guest("Alice", "alice@example.com", "123-456-7890", rabbitmq.get_connection_params())
