"""
05_resilience_testing.py - Demonstrates RabbitMQ resilience testing with Testcontainers.

This example tests RabbitMQ's durability and reconnection handling after failures.
"""

import pytest
import pika
import time

def test_rabbitmq_resilience(rabbitmq_connection, rabbitmq_container):
    """Test RabbitMQ resilience by sending a message, restarting RabbitMQ, and verifying persistence."""
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue="resilience_queue", durable=True)
    
    channel.basic_publish(exchange='', routing_key="resilience_queue", body="Resilience Test Message",
                          properties=pika.BasicProperties(delivery_mode=2))
    
    rabbitmq_container.stop()
    time.sleep(5)  # Simulate downtime
    
    rabbitmq_container.start()
    time.sleep(5)  # Allow RabbitMQ to restart
    
    method_frame, header_frame, body = channel.basic_get(queue="resilience_queue", auto_ack=True)
    assert body is not None
    assert body.decode("utf-8") == "Resilience Test Message"