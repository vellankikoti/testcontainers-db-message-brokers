"""
04_occupancy_report.py - Occupancy Report System

This example demonstrates an occupancy report system using RabbitMQ and Testcontainers.
It tests generating occupancy reports by sending messages to a RabbitMQ queue.
"""

import pika
import time

def generate_occupancy_report(connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='occupancy_report')

    message = "Occupancy report generated"
    channel.basic_publish(exchange='', routing_key='occupancy_report', body=message)
    print("[x] Occupancy report generated successfully")

    connection.close()

def test_generate_occupancy_report(rabbitmq_container):
    """Test generating an occupancy report."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Generate an occupancy report using the RabbitMQ container's connection parameters
    generate_occupancy_report(rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='occupancy_report')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='occupancy_report', auto_ack=True)
    expected_message = "Occupancy report generated"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        generate_occupancy_report(rabbitmq.get_connection_params())
