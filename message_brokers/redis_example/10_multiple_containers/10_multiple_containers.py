import json
import redis
import logging
from testcontainers.core.container import DockerContainer
import time

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

def get_data(redis_client, key):
    """Get data from Redis."""
    value = redis_client.get(key)
    return json.loads(value) if value else None

def test_multiple_containers():
    """Test interactions between multiple Redis containers."""
    logging.info("Starting multiple Redis containers for testing...")

    with DockerContainer("redis:latest") as redis_container1, \
         DockerContainer("redis:latest") as redis_container2:

        # Expose ports for both containers
        redis_container1.with_exposed_ports(6379)
        redis_container2.with_exposed_ports(6379)

        # Start the containers
        redis_container1.start()
        redis_container2.start()

        # Get the host and port for both containers
        host1 = redis_container1.get_container_host_ip()
        port1 = redis_container1.get_exposed_port(6379)

        host2 = redis_container2.get_container_host_ip()
        port2 = redis_container2.get_exposed_port(6379)

        # Create Redis clients for both containers
        redis_client1 = redis.Redis(host=host1, port=port1)
        redis_client2 = redis.Redis(host=host2, port=port2)

        logging.info("Waiting for Redis containers to be ready...")
        if not wait_for_redis(redis_client1) or not wait_for_redis(redis_client2):
            logs1 = redis_container1.get_logs()
            logs2 = redis_container2.get_logs()
            logging.error(f"Redis container 1 logs:\n{logs1.decode('utf-8')}")
            logging.error(f"Redis container 2 logs:\n{logs2.decode('utf-8')}")
            raise Exception("One or both Redis containers did not start in time.")

        # Add data to the first Redis container
        add_data(redis_client1, 'key1', {'name': 'Alice'})
        add_data(redis_client1, 'key2', {'name': 'Bob'})

        # Retrieve data from the first container
        data1_key1 = get_data(redis_client1, 'key1')
        data1_key2 = get_data(redis_client1, 'key2')
        logging.info(f"Retrieved from Redis 1: key1 -> {data1_key1}, key2 -> {data1_key2}")

        # Migrate data from the first container to the second container
        add_data(redis_client2, 'key1', data1_key1)
        add_data(redis_client2, 'key2', data1_key2)

        # Retrieve data from the second container
        data2_key1 = get_data(redis_client2, 'key1')
        data2_key2 = get_data(redis_client2, 'key2')
        logging.info(f"Retrieved from Redis 2: key1 -> {data2_key1}, key2 -> {data2_key2}")

if __name__ == "__main__":
    test_multiple_containers()
