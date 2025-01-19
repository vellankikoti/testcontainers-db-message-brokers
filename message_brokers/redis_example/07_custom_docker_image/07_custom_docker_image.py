import json
import redis
import logging
import time
from testcontainers.core.container import DockerContainer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_LIST = 'custom_docker_image_data'

def add_data(redis_client, data):
    """Add data to Redis."""
    redis_client.rpush(REDIS_LIST, json.dumps(data))
    logging.info(f"Added data: {data}")

def view_data(redis_client):
    """View all data in Redis."""
    data = redis_client.lrange(REDIS_LIST, 0, -1)
    return [json.loads(item) for item in data]

def wait_for_redis(redis_client, timeout=60):
    """Wait for Redis to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try to ping the Redis server
            if redis_client.ping():
                logging.info("Redis is ready.")
                return True
        except redis.ConnectionError:
            logging.warning("Redis is not ready yet, retrying...")
            time.sleep(1)  # Wait before retrying
    logging.error("Redis did not become ready in time.")
    return False

def test_custom_docker_image():
    """Test the custom Docker image functionality."""
    # Use the custom Redis image for testing
    with DockerContainer("custom-redis-image:latest") as redis_container:
        # Expose the Redis default port
        redis_container.with_exposed_ports(6379)

        # Start the container
        redis_container.start()

        # Retrieve container host and port
        redis_host = redis_container.get_container_host_ip()
        redis_port = redis_container.get_exposed_port(6379)

        redis_client = redis.Redis(host=redis_host, port=redis_port)

        # Wait for Redis to be ready
        if not wait_for_redis(redis_client):
            raise Exception("Redis container did not start in time.")

        # Clear the Redis list before the test
        redis_client.delete(REDIS_LIST)

        # Test Case: Add data and view it
        add_data(redis_client, {"id": 1, "name": "Test Data"})
        data = view_data(redis_client)
        assert len(data) == 1
        assert data[0]['id'] == 1
        assert data[0]['name'] == "Test Data"

        logging.info("Test case executed successfully!")

if __name__ == "__main__":
    test_custom_docker_image()
