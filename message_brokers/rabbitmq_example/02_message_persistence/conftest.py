"""
conftest.py - Pytest fixture for RabbitMQ using Testcontainers.

Fixes:
- Ensures RabbitMQ messages persist across restart.
- Uses volume mapping instead of `with_tmpfs()` (fix for RabbitMqContainer issue).
"""

import time
import pytest
import pika
import requests
from testcontainers.core.container import DockerContainer  # ✅ Use Generic DockerContainer
from testcontainers.rabbitmq import RabbitMqContainer
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.fixture(scope="module")
def rabbitmq_container():
    """
    Pytest fixture to start a RabbitMQ container and ensure it is ready.
    Uses volume mapping to persist RabbitMQ messages across restart.
    """
    container = DockerContainer("rabbitmq:3.11-management") \
        .with_bind_ports(5672, 5672) \
        .with_bind_ports(15672, 15672) \
        .with_volume_mapping("/tmp/rabbitmq_data", "/var/lib/rabbitmq")  # ✅ Persistent storage fix

    container.start()
    wait_for_logs(container, "Server startup complete", timeout=30)
    wait_for_rabbitmq_management(container)

    yield container  # Provide container to test

    container.stop()


def wait_for_rabbitmq_management(container, retries=10, delay=5):
    """
    Wait until RabbitMQ Management UI is available.
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
