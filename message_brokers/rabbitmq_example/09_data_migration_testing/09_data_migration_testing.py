"""
09_data_migration_testing.py - Data Migration Testing

This example demonstrates testing data migration using RabbitMQ and Testcontainers.
It tests sending migration messages to a RabbitMQ queue.
"""

import pika
import time

def migrate_data(data, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='data_migration')

    message = f"Data migration: {data}"
    channel.basic_publish(exchange='', routing_key='data_migration', body=message)
    print(f"[x] Data migration message sent: {data}")

    connection.close()

def test_migrate_data(rabbitmq_container):
    """Test data migration."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Migrate data using the RabbitMQ container's connection parameters
    data = "User data from old system"
    migrate_data(data, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='data_migration')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='data_migration', auto_ack=True)
    expected_message = f"Data migration: {data}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        migrate_data("User data from old system", rabbitmq.get_connection_params())
