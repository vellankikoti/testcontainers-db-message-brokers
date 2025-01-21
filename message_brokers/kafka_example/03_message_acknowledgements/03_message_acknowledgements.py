"""
03_message_acknowledgements.py - Demonstrates Kafka message acknowledgements with Testcontainers.

This example verifies that Kafka only commits messages after explicit acknowledgment.
"""

import pytest
import time

def test_kafka_message_acknowledgement(kafka_producer, kafka_consumer):
    """Test that messages are only committed after acknowledgment."""
    test_message = "Acknowledged Message"
    kafka_producer.send("test_topic", test_message)
    kafka_producer.flush()
    
    time.sleep(2)  # Allow time for message propagation
    
    for message in kafka_consumer:
        assert message.value == test_message
        kafka_consumer.commit()  # Explicit acknowledgment
        break  # Exit after verifying the first message
    
    # Ensure that after acknowledgment, the message is not received again
    kafka_consumer.seek_to_beginning()
    messages_after_ack = [msg for msg in kafka_consumer]
    assert len(messages_after_ack) == 0  # No reprocessing of acknowledged messages