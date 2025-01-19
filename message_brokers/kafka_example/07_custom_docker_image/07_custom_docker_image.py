import pytest
from testcontainers.kafka import KafkaContainer
from kafka import KafkaProducer, KafkaConsumer
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def kafka_container():
    """Fixture to manage Kafka container lifecycle."""
    logger.info("Starting Kafka container...")

    with KafkaContainer("confluentinc/cp-kafka:latest") as container:
        # Get the bootstrap servers for the Kafka container
        bootstrap_servers = container.get_bootstrap_server()
        logger.info(f"Kafka container started. Bootstrap servers: {bootstrap_servers}")
        yield bootstrap_servers

@pytest.fixture(scope="module")
def kafka_producer(kafka_container):
    """Create a Kafka producer connected to the container."""
    producer = KafkaProducer(
        bootstrap_servers=kafka_container,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    yield producer
    producer.close()

@pytest.fixture(scope="module")
def kafka_consumer(kafka_container):
    """Create a Kafka consumer connected to the container."""
    consumer = KafkaConsumer(
        'custom_topic',
        bootstrap_servers=kafka_container,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    yield consumer
    consumer.close()

def produce_messages(producer):
    """Produce messages to the Kafka topic."""
    for i in range(5):
        message = {'number': i}
        producer.send('custom_topic', value=message)
        logger.info(f"Produced: {message}")
        time.sleep(1)  # Simulate some delay

def consume_messages(consumer):
    """Consume messages from the Kafka topic."""
    messages = []
    for _ in range(5):  # Consume 5 messages
        message = next(consumer)
        messages.append(message.value)
        logger.info(f"Consumed: {message.value}")
    return messages

def test_kafka_producer_consumer(kafka_producer, kafka_consumer):
    """Test producing and consuming messages."""
    logger.info("Running test_kafka_producer_consumer")

    # Produce messages
    produce_messages(kafka_producer)

    # Consume messages
    consumed_messages = consume_messages(kafka_consumer)

    # Verify the messages
    expected_messages = [{'number': i} for i in range(5)]
    assert consumed_messages == expected_messages

    logger.info("Kafka producer-consumer test passed")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
