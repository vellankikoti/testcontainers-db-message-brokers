"""
02_message_persistence.py - Demonstrates RabbitMQ message persistence with Testcontainers.

This example verifies that RabbitMQ retains messages even after container restarts.
"""

import pytest
import pika
import time

def test_rabbitmq_message_persistence(rabbitmq_connection, rabbitmq_container):
    """Test that messages persist in RabbitMQ even after a restart."""
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue="persistent_queue", durable=True)
    
    channel.basic_publish(exchange='', routing_key="persistent_queue", body="Persistent Message",
                          properties=pika.BasicProperties(delivery_mode=2))
    
    rabbitmq_container.stop()
    time.sleep(5)  # Simulate downtime
    rabbitmq_container.start()
    time.sleep(5)  # Allow RabbitMQ to restart
    
    method_frame, header_frame, body = channel.basic_get(queue="persistent_queue", auto_ack=True)
    assert body is not None
    assert body.decode("utf-8") == "Persistent Message"