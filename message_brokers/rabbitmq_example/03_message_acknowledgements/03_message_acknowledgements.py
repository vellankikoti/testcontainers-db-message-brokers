"""
03_message_acknowledgements.py - Demonstrates RabbitMQ message acknowledgements with Testcontainers.

This example verifies that messages are acknowledged properly.
"""

import pytest
import pika
import time

def test_rabbitmq_message_acknowledgement(rabbitmq_connection):
    """Test that messages in RabbitMQ require explicit acknowledgments."""
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue="ack_queue")
    
    channel.basic_publish(exchange='', routing_key="ack_queue", body="Acknowledgement Test Message")
    
    def callback(ch, method, properties, body):
        assert body.decode("utf-8") == "Acknowledgement Test Message"
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel.basic_consume(queue="ack_queue", on_message_callback=callback, auto_ack=False)
    
    method_frame, header_frame, body = channel.basic_get(queue="ack_queue", auto_ack=False)
    assert body is not None
    assert body.decode("utf-8") == "Acknowledgement Test Message"
    
    # Manually acknowledge the message
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)