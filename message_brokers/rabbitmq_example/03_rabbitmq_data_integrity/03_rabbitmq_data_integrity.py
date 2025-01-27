import time
import pytest
import pika
from testcontainers.rabbitmq import RabbitMQContainer

QUEUE_NAME = "data_integrity_queue"

@pytest.fixture(scope="module")
def rabbitmq_url():
    """ Starts RabbitMQ container and provides AMQP URL """
    with RabbitMQContainer("rabbitmq:latest") as rabbitmq:
        yield rabbitmq.get_connection_url()

def publish_messages(rabbitmq_url):
    """ Publishes messages to RabbitMQ """
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    messages = ["Message 1", "Message 2", "Message 3"]
    for msg in messages:
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=msg)
        print(f"Produced: {msg}")

    connection.close()
    return messages

def consume_messages(rabbitmq_url):
    """ Consumes messages from RabbitMQ """
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    received_messages = []
    for method_frame, properties, body in channel.consume(QUEUE_NAME, auto_ack=True):
        received_messages.append(body.decode())
        print(f"Consumed: {body.decode()}")

        if len(received_messages) == 3:
            break

    connection.close()
    return received_messages

def test_data_integrity(rabbitmq_url):
    """ Validates RabbitMQ message integrity """
    sent_messages = publish_messages(rabbitmq_url)
    time.sleep(5)  # Simulating delay

    received_messages = consume_messages(rabbitmq_url)

    assert received_messages == sent_messages, "Message order was not preserved!"
    assert len(received_messages) == len(set(received_messages)), "Duplicate messages detected!"
    assert set(received_messages) == set(sent_messages), "Some messages are missing!"

    print("\n✅ RabbitMQ Data Integrity Test Passed!")
