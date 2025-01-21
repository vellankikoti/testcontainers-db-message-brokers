"""
01_basic_pubsub.py - Demonstrates basic RabbitMQ Pub/Sub with Testcontainers.

This example tests message publishing and consuming in RabbitMQ.
"""

import pytest
import pika
import time

def test_rabbitmq_pubsub(rabbitmq_connection):
    """Test that a message published to RabbitMQ is received by a consumer."""
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue="test_queue")
    
    channel.basic_publish(exchange='', routing_key="test_queue", body="Hello, RabbitMQ!")
    
    time.sleep(2)  # Allow time for message propagation
    
    method_frame, header_frame, body = channel.basic_get(queue="test_queue", auto_ack=True)
    assert body is not None
    assert body.decode("utf-8") == "Hello, RabbitMQ!"