"""
06_simulating_failures.py - Simulating Failures

This example demonstrates simulating failures in the system using RabbitMQ and Testcontainers.
It tests how the system handles failure messages by sending messages to a RabbitMQ queue.
"""

import pika
import time

def simulate_failure(failure_type, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='failure_simulation')

    message = f"Simulated failure: {failure_type}"
    channel.basic_publish(exchange='', routing_key='failure_simulation', body=message)
    print(f"[x] Failure simulated: {failure_type}")

    connection.close()

def test_simulate_failure(rabbitmq_container):
    """Test simulating a failure."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Simulate a failure using the RabbitMQ container's connection parameters
    failure_type = "Network Error"
    simulate_failure(failure_type, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='failure_simulation')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='failure_simulation', auto_ack=True)
    expected_message = f"Simulated failure: {failure_type}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        simulate_failure("Network Error", rabbitmq.get_connection_params())
