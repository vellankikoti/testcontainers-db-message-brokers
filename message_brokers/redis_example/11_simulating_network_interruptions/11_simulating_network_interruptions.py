import json
import redis
import logging
from testcontainers.core.container import DockerContainer
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_redis(redis_client, timeout=60):
    """Wait for Redis to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if redis_client.ping():
                logging.info("Redis is ready.")
                return True
        except redis.ConnectionError:
            logging.warning("Redis is not ready yet, retrying...")
            time.sleep(1)
    logging.error("Redis did not become ready in time.")
    return False

def add_data(redis_client, key, value):
    """Add data to Redis."""
    redis_client.set(key, json.dumps(value))
    logging.info(f"Added {key}: {value}")

def simulate_network_interruption():
    """Randomly simulate a network interruption."""
    if random.choice([True, False]):
        logging.warning("Simulating network interruption...")
        raise redis.ConnectionError("Simulated network interruption")

def test_network_interruptions():
    """Test network interruptions with Redis."""
    logging.info("Starting the Redis container for network interruption testing...")
    with DockerContainer("redis:latest") as redis_container:
        redis_container.with_exposed_ports(6379)
        redis_container.start()

        redis_host = redis_container.get_container_host_ip()
        redis_port = redis_container.get_exposed_port(6379)

        redis_client = redis.Redis(host=redis_host, port=redis_port)

        logging.info("Waiting for Redis to be ready...")
        if not wait_for_redis(redis_client):
            logs = redis_container.get_logs()
            logging.error(f"Redis logs:\n{logs.decode('utf-8')}")
            raise Exception("Redis container did not start in time.")

        # Add data and simulate network interruptions
        for i in range(5):
            try:
                simulate_network_interruption()
                add_data(redis_client, f'key{i}', {'value': f'Data {i}'})
                logging.info(f"Added key{i} successfully.")
            except redis.ConnectionError as e:
                logging.error(f"Failed to add key{i}: {e}")

        # Verify data retrieval
        for i in range(5):
            try:
                simulate_network_interruption()
                value = redis_client.get(f'key{i}')
                logging.info(f"Retrieved key{i}: {value.decode('utf-8') if value else 'None'}")
            except redis.ConnectionError as e:
                logging.error(f"Failed to retrieve key{i}: {e}")

if __name__ == "__main__":
    test_network_interruptions()
