"""
04_performance_testing.py - Demonstrates RabbitMQ performance testing with Testcontainers.

This example measures message throughput in RabbitMQ.
"""

import pytest
import pika
import time

def test_rabbitmq_performance(rabbitmq_connection):
    """Test RabbitMQ performance by measuring message publish rate."""
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue="performance_queue")
    
    num_messages = 10000
    start_time = time.time()
    
    for i in range(num_messages):
        channel.basic_publish(exchange='', routing_key="performance_queue", body=f"Message {i}")
    
    duration = time.time() - start_time
    print(f"Published {num_messages} messages in {duration:.2f} seconds")
    
    assert duration < 10  # Expect the messages to be published within 10 seconds