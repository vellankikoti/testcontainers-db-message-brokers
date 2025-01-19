"""
03_reservations.py - Reservation System

This example demonstrates a reservation system using RabbitMQ and Testcontainers.
It tests handling reservation requests by sending messages to a RabbitMQ queue.
"""

import pika
import time

def make_reservation(guest_name, room_number, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='reservations')

    message = f"Reservation made for {guest_name} in room {room_number}"
    channel.basic_publish(exchange='', routing_key='reservations', body=message)
    print(f"[x] Reservation made successfully for: {guest_name}")

    connection.close()

def test_make_reservation(rabbitmq_container):
    """Test making a reservation."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Make a reservation using the RabbitMQ container's connection parameters
    guest_name = "Alice"
    room_number = "101"
    make_reservation(guest_name, room_number, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='reservations')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='reservations', auto_ack=True)
    expected_message = f"Reservation made for {guest_name} in room {room_number}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        make_reservation("Alice", "101", rabbitmq.get_connection_params())
