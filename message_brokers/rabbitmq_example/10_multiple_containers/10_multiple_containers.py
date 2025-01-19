"""
10_multiple_containers.py - Multiple Containers Example

This example demonstrates using multiple RabbitMQ containers with Testcontainers.
It tests sending messages between two RabbitMQ queues.
"""

import pika
import time

def send_message(queue_name, message, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(f"[x] Message sent to {queue_name}: {message}")

    connection.close()

def test_multiple_containers(rabbitmq_container):
    """Test sending messages between multiple containers."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send messages to two different queues
    send_message('queue_one', 'Message for Queue One', rabbitmq_container.get_connection_params())
    send_message('queue_two', 'Message for Queue Two', rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the messages
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queues
    channel.queue_declare(queue='queue_one')
    channel.queue_declare(queue='queue_two')

    # Verify the messages were sent
    method_frame, header_frame, body = channel.basic_get(queue='queue_one', auto_ack=True)
    assert body.decode() == 'Message for Queue One'

    method_frame, header_frame, body = channel.basic_get(queue='queue_two', auto_ack=True)
    assert body.decode() == 'Message for Queue Two'

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        send_message('queue_one', 'Message for Queue One', rabbitmq.get_connection_params())
        send_message('queue_two', 'Message for Queue Two', rabbitmq.get_connection_params())
