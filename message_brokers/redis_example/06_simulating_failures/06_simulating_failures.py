import json
import redis
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_LIST = 'simulated_failures'

def add_data(redis_client, data):
    """Add data to Redis."""
    redis_client.rpush(REDIS_LIST, json.dumps(data))
    logging.info(f"Added data: {data}")

def simulate_connection_failure(redis_client, force_failure=False):
    """Simulate a connection failure."""
    try:
        # Simulate a connection failure
        if force_failure or random.choice([True, False]):
            raise redis.ConnectionError("Simulated connection failure.")
        logging.info("Connection successful.")
    except redis.ConnectionError as e:
        logging.error(f"Connection error: {e}")
        return False
    return True

def simulate_timeout(redis_client, force_timeout=False):
    """Simulate a timeout scenario."""
    try:
        # Simulate a timeout
        if force_timeout:
            time.sleep(2)  # Simulate a delay
            raise redis.TimeoutError("Simulated timeout error.")
        else:
            time.sleep(1)  # Simulate a normal operation
            logging.info("Operation completed successfully.")
    except redis.TimeoutError as e:
        logging.error(f"Timeout error: {e}")
        return False
    return True

def simulate_data_corruption(redis_client):
    """Simulate data corruption."""
    try:
        # Simulate data corruption
        data = redis_client.lrange(REDIS_LIST, 0, -1)
        if data:
            corrupted_data = data[0].decode('utf-8') + " corrupted"
            redis_client.lset(REDIS_LIST, 0, corrupted_data)
            logging.info("Data corrupted.")
        else:
            logging.warning("No data to corrupt.")
    except Exception as e:
        logging.error(f"Error during data corruption simulation: {e}")

# Test cases
def test_simulating_failures(redis_container):
    """Test the failure simulation functionality."""
    redis_client = redis_container

    # Clear the Redis list before the test
    redis_client.delete(REDIS_LIST)

    # Test Case 1: Simulate connection failure
    assert not simulate_connection_failure(redis_client, force_failure=True)  # Force a failure

    # Test Case 2: Add data and simulate timeout
    add_data(redis_client, {"id": 1, "name": "Test Data"})
    assert not simulate_timeout(redis_client, force_timeout=True)  # Force a timeout

    # Test Case 3: Simulate data corruption
    add_data(redis_client, {"id": 2, "name": "More Test Data"})
    simulate_data_corruption(redis_client)
    corrupted_data = redis_client.lindex(REDIS_LIST, 0).decode('utf-8')
    assert "corrupted" in corrupted_data  # Check if data is corrupted

if __name__ == "__main__":
    # Initialize Redis client (assuming redis_container is available)
    redis_client = redis.Redis(host='localhost', port=6379)  # Adjust as necessary for your setup

    # Example usage
    add_data(redis_client, {"id": 1, "name": "Initial Data"})
    simulate_connection_failure(redis_client, force_failure=True)
    assert not simulate_timeout(redis_client, force_timeout=True)  # Force a timeout
    simulate_data_corruption(redis_client)
