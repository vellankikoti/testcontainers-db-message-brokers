"""
conftest.py - Pytest fixture for RabbitMQ using Testcontainers.

Provides:
- A RabbitMQ container that starts before tests and stops afterward.
- Ensures RabbitMQ is fully ready before running tests.
- Reusable fixture for RabbitMQ connections.
"""

import time
import pytest
import pika
import requests
from testcontainers.rabbitmq import RabbitMqContainer
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.fixture(scope="module")
def rabbitmq_container():
    """
    Pytest fixture to start a RabbitMQ container and ensure it is ready.
    Returns:
        RabbitMqContainer: Running RabbitMQ container.
    """
    container = RabbitMqContainer("rabbitmq:3.11-management") \
        .with_bind_ports(5672, 5672) \
        .with_bind_ports(15672, 15672)

    container.start()
    wait_for_logs(container, "Server startup complete", timeout=30)
    wait_for_rabbitmq_management(container)

    yield container
    container.stop()


def wait_for_rabbitmq_management(container, retries=10, delay=5):
    """
    Wait until RabbitMQ Management UI is available.

    Args:
        container (RabbitMqContainer): Running RabbitMQ container.
        retries (int): Max retries.
        delay (int): Delay between retries.

    Returns:
        bool: True if RabbitMQ UI is reachable.
    """
    management_url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(15672)}"

    for attempt in range(retries):
        try:
            response = requests.get(management_url, timeout=3)
            if response.status_code == 200:
                print(f"✅ RabbitMQ UI Ready: {management_url}")
                return True
        except requests.ConnectionError:
            print(f"⏳ Waiting for RabbitMQ UI... ({attempt + 1}/{retries})")
        time.sleep(delay)

    raise TimeoutError("❌ RabbitMQ Management UI did not become available.")


def get_rabbitmq_connection(container, retries=5, delay=5):
    """
    Establish a connection to RabbitMQ with retries.

    Args:
        container (RabbitMqContainer): Running RabbitMQ container.
        retries (int): Number of connection retries.
        delay (int): Delay between retries.

    Returns:
        pika.BlockingConnection: Connection to RabbitMQ.
    """
    credentials = pika.PlainCredentials("guest", "guest")
    connection_params = pika.ConnectionParameters(
        host=container.get_container_host_ip(),
        port=int(container.get_exposed_port(5672)),
        virtual_host="/",
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )

    for attempt in range(retries):
        try:
            return pika.BlockingConnection(connection_params)
        except pika.exceptions.AMQPConnectionError:
            print(f"🔁 Retrying RabbitMQ connection ({attempt + 1}/{retries})...")
            time.sleep(delay)

    raise ConnectionError("❌ Failed to establish RabbitMQ connection after multiple attempts.")
