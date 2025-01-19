"""
12_distributed_transactions.py - Distributed Transactions

This example demonstrates handling distributed transactions using RabbitMQ and Testcontainers.
It tests sending transaction messages to a RabbitMQ queue.
"""

import pika
import time

def process_transaction(transaction_id, amount, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='distributed_transactions')

    message = f"Transaction ID: {transaction_id}, Amount: {amount}"
    channel.basic_publish(exchange='', routing_key='distributed_transactions', body=message)
    print(f"[x] Processed transaction: {transaction_id}")

    connection.close()

def test_process_transaction(rabbitmq_container):
    """Test processing a distributed transaction."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Process a transaction using the RabbitMQ container's connection parameters
    transaction_id = "TX12345"
    amount = 100.0
    process_transaction(transaction_id, amount, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='distributed_transactions')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='distributed_transactions', auto_ack=True)
    expected_message = f"Transaction ID: {transaction_id}, Amount: {amount}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        process_transaction("TX12345", 100.0, rabbitmq.get_connection_params())
