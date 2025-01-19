import json
import redis
import logging
import time
from testcontainers.core.container import DockerContainer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_LIST = 'performance_testing_data'

def add_data(redis_client, data):
    """Add data to Redis."""
    redis_client.rpush(REDIS_LIST, json.dumps(data))

def view_data(redis_client):
    """View all data in Redis."""
    data = redis_client.lrange(REDIS_LIST, 0, -1)
    return [json.loads(item) for item in data]

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
            time.sleep(1)  # Wait before retrying
    logging.error("Redis did not become ready in time.")
    return False

def performance_test(redis_client, num_entries):
    """Perform performance testing by adding and retrieving data."""
    # Measure time to add data
    start_time = time.time()
    for i in range(num_entries):
        add_data(redis_client, {"id": i, "name": f"Test Data {i}"})
    add_duration = time.time() - start_time
    logging.info(f"Added {num_entries} entries in {add_duration:.2f} seconds.")

    # Measure time to retrieve data
    start_time = time.time()
    data = view_data(redis_client)
    retrieve_duration = time.time() - start_time
    logging.info(f"Retrieved {len(data)} entries in {retrieve_duration:.2f} seconds.")

def test_performance_testing():
    """Test the performance of Redis operations."""
    logging.info("Starting the Redis container for performance testing...")
    with DockerContainer("custom-redis-image:latest") as redis_container:
        # Bind the Redis default port (6379) and expose it
        redis_container.with_exposed_ports(6379)

        # Start the container
        redis_container.start()

        # Get the host and port
        redis_host = redis_container.get_container_host_ip()
        redis_port = redis_container.get_exposed_port(6379)

        logging.info(f"Redis container started. Host: {redis_host}, Port: {redis_port}")

        redis_client = redis.Redis(host=redis_host, port=redis_port)

        # Wait for Redis to be ready
        logging.info("Waiting for Redis to be ready...")
        if not wait_for_redis(redis_client):
            # Print container logs for debugging if Redis is not ready
            logs = redis_container.get_logs()
            logging.error(f"Redis logs:\n{logs.decode('utf-8')}")
            raise Exception("Redis container did not start in time.")

        # Perform performance testing
        num_entries = 10000  # Number of entries to test
        performance_test(redis_client, num_entries)

if __name__ == "__main__":
    test_performance_testing()
