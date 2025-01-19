"""
14_security_testing.py - Security Testing

This example demonstrates security testing using RabbitMQ and Testcontainers.
It tests sending security-related messages to a RabbitMQ queue.
"""

import pika
import time

def send_security_alert(alert_type, details, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='security_alerts')

    message = f"Alert Type: {alert_type}, Details: {details}"
    channel.basic_publish(exchange='', routing_key='security_alerts', body=message)
    print(f"[x] Security alert sent: {alert_type}")

    connection.close()

def test_send_security_alert_unauthorized_access(rabbitmq_container):
    """Test sending an unauthorized access alert."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send a security alert for unauthorized access
    alert_type = "Unauthorized Access"
    details = "User attempted to access restricted area"
    send_security_alert(alert_type, details, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='security_alerts')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='security_alerts', auto_ack=True)
    expected_message = f"Alert Type: {alert_type}, Details: {details}"
    assert body.decode() == expected_message

    connection.close()

def test_send_security_alert_data_breach(rabbitmq_container):
    """Test sending a data breach alert."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send a security alert for a data breach
    alert_type = "Data Breach"
    details = "Sensitive data exposed"
    send_security_alert(alert_type, details, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='security_alerts')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='security_alerts', auto_ack=True)
    expected_message = f"Alert Type: {alert_type}, Details: {details}"
    assert body.decode() == expected_message

    connection.close()

def test_send_security_alert_malicious_activity(rabbitmq_container):
    """Test sending a malicious activity alert."""
    # Wait for RabbitMQ to be ready
    time.sleep(5)  # Adjust as necessary for your environment

    # Send a security alert for malicious activity
    alert_type = "Malicious Activity"
    details = "Suspicious login attempts detected"
    send_security_alert(alert_type, details, rabbitmq_container.get_connection_params())

    # Connect to the RabbitMQ container to verify the message
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='security_alerts')

    # Verify the message was sent
    method_frame, header_frame, body = channel.basic_get(queue='security_alerts', auto_ack=True)
    expected_message = f"Alert Type: {alert_type}, Details: {details}"
    assert body.decode() == expected_message

    connection.close()

if __name__ == "__main__":
    # Example usage
    with RabbitMqContainer("rabbitmq:3.9.10") as rabbitmq:
        send_security_alert("Unauthorized Access", "User attempted to access restricted area", rabbitmq.get_connection_params())
