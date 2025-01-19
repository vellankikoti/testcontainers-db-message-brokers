"""
11_simulating_network_interruptions.py - Simulating Network Interruptions

This example demonstrates simulating network interruptions using RabbitMQ and Testcontainers.
It tests how the system handles messages during network issues.
"""

import pika
import time

def simulate_network_issue(issue_type, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='network_issues')

    message = f"Simulated network issue: {issue_type}"
    channel.basic_publish(exchange='', routing_key='network_issues', body=message)
    print(f"[x] Network issue simulated: {issue_type}")

    connection.close()

def test_simulate_network_issue(rabbitmq_container):
    """Test simulating a network issue."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Simulate a network issue using the RabbitMQ container's connection parameters
    issue_type = "Connection Timeout"
    simulate_network_issue(issue_type, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='network_issues')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='network_issues', auto_ack=True)
    expected_message = f"Simulated network issue: {issue_type}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        simulate_network_issue("Connection Timeout", rabbitmq.get_connection_params())
