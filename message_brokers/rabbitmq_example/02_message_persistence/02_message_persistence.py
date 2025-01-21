"""
02_room_management.py - Room Management System

This example demonstrates a room management system using RabbitMQ and Testcontainers.
It tests the management of room details by sending messages to a RabbitMQ queue.
"""

import pika
import time

def manage_room(room_number, room_type, action, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='room_management')

    message = f"{action} room: Number: {room_number}, Type: {room_type}"
    channel.basic_publish(exchange='', routing_key='room_management', body=message)
    print(f"[x] {action} room successfully: {room_number}")

    connection.close()

def test_manage_room(rabbitmq_container):
    """Test managing a room."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Manage a room using the RabbitMQ container's connection parameters
    room_number = "101"
    room_type = "Deluxe"
    action = "Add"
    manage_room(room_number, room_type, action, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='room_management')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='room_management', auto_ack=True)
    expected_message = f"{action} room: Number: {room_number}, Type: {room_type}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        manage_room("101", "Deluxe", "Add", rabbitmq.get_connection_params())
