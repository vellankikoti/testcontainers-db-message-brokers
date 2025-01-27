"""
conftest.py - Shared fixture for Kafka Testcontainers.
"""

import pytest
import time
from testcontainers.kafka import KafkaContainer
from kafka import KafkaAdminClient
from kafka.errors import KafkaError


@pytest.fixture(scope="session")
def kafka_container():
    """Starts a fully working Kafka container for testing."""
    with KafkaContainer("confluentinc/cp-kafka:7.6.0") as kafka:
        # Set required environment variables
        kafka.with_env("KAFKA_AUTO_CREATE_TOPICS_ENABLE", "true")
        kafka.with_env("KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR", "1")
        kafka.with_env("KAFKA_LISTENERS", "PLAINTEXT://0.0.0.0:9092")
        kafka.with_env("KAFKA_ADVERTISED_LISTENERS", "PLAINTEXT://localhost:9092")
        kafka.with_env("KAFKA_ZOOKEEPER_CONNECT", "localhost:2181")  # Required for Kafka 7.x
        
        kafka.with_exposed_ports(9092)  # Ensure Kafka port is accessible
        kafka.with_network_mode("bridge")  # Avoid Docker networking issues
        
        kafka.start()
        
        # **Explicit wait for Kafka readiness using Admin API**
        max_wait = 40  # Increased timeout for slow environments
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                admin_client = KafkaAdminClient(bootstrap_servers=kafka.get_bootstrap_server())
                topics = admin_client.list_topics()
                if topics is not None:  # Ensure Kafka is responding
                    break
            except KafkaError:
                time.sleep(2)  # Retry every 2 seconds
        
        yield kafka.get_bootstrap_server()
