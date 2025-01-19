"""
05_extended_stays.py - Extended Stays Management

This example demonstrates managing extended stays using RabbitMQ and Testcontainers.
It tests handling requests for extending stays by sending messages to a RabbitMQ queue.
"""

import pika
import time

def extend_stay(guest_name, room_number, new_end_date, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='extended_stays')

    message = f"Extended stay for {guest_name} in room {room_number} until {new_end_date}"
    channel.basic_publish(exchange='', routing_key='extended_stays', body=message)
    print(f"[x] Stay extended successfully for: {guest_name}")

    connection.close()

def test_extend_stay(rabbitmq_container):
    """Test extending a stay."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Extend a stay using the RabbitMQ container's connection parameters
    guest_name = "Alice"
    room_number = "101"
    new_end_date = "2024-12-31"
    extend_stay(guest_name, room_number, new_end_date, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='extended_stays')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='extended_stays', auto_ack=True)
    expected_message = f"Extended stay for {guest_name} in room {room_number} until {new_end_date}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        extend_stay("Alice", "101", "2024-12-31", rabbitmq.get_connection_params())
