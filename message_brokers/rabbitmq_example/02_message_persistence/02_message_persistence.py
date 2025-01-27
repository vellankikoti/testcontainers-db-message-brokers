"""
02_message_persistence.py - RabbitMQ Message Persistence Test

Fixes:
- Ensures messages persist across RabbitMQ restart.
- Uses tmpfs to keep RabbitMQ state during restart.
"""

import time
import pytest
import pika
from conftest import get_rabbitmq_connection


def test_rabbitmq_message_persistence(rabbitmq_container):
    """
    Test that RabbitMQ retains messages after restart.
    """
    queue_name = "persistent_queue"

    # Step 1: Publish Messages to Durable Queue
    print("\n🚀 Publishing persistent messages to RabbitMQ...")
    connection = get_rabbitmq_connection(rabbitmq_container)
    channel = connection.channel()

    # Declare Durable Queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish Persistent Message
    persistent_message = "Persistent Message"
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=persistent_message,
        properties=pika.BasicProperties(delivery_mode=2),  # Persistent message
    )
    connection.close()
    print("✅ Message successfully published!")

    # Step 2: Verify Message Exists Before Restart
    connection = get_rabbitmq_connection(rabbitmq_container)
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, durable=True)
    message_count = queue.method.message_count
    connection.close()

    assert message_count > 0, "❌ Message was lost before restart!"
    print(f"✅ {message_count} messages found in queue before restart!")

    # Step 3: Stop and Restart RabbitMQ
    print("\n⏳ Stopping RabbitMQ container...")
    rabbitmq_container.stop(kill=False)  # 🔥 Stop without deleting data
    time.sleep(5)  # Simulate downtime
    print("❌ RabbitMQ container stopped.")

    print("\n🔄 Restarting RabbitMQ container...")
    rabbitmq_container.start()
    time.sleep(5)
    print("✅ RabbitMQ container restarted successfully!")

    # Step 4: Consume Messages After Restart
    print("\n🔍 Consuming messages from RabbitMQ after restart...")
    connection = get_rabbitmq_connection(rabbitmq_container)
    channel = connection.channel()

    # Declare the Durable Queue Again
    channel.queue_declare(queue=queue_name, durable=True)

    # Retrieve the Persisted Message
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    connection.close()

    # Step 5: Validate Message Persistence
    assert body == persistent_message.encode(), "❌ Message was not persisted after RabbitMQ restart!"
    print("✅ Message successfully retrieved after restart! Persistence confirmed.")
