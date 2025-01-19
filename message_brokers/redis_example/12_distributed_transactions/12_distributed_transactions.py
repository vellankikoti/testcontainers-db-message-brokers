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

def perform_transaction(redis_client):
    """Perform a distributed transaction in Redis."""
    with redis_client.pipeline() as pipe:
        try:
            # Start a transaction
            pipe.multi()
            # Set multiple keys
            pipe.set('transaction_key1', json.dumps({'name': 'Alice'}))
            pipe.set('transaction_key2', json.dumps({'name': 'Bob'}))
            # Increment a counter
            pipe.incr('transaction_counter')
            # Execute the transaction
            pipe.execute()
            logging.info("Transaction executed successfully.")
        except redis.RedisError as e:
            logging.error(f"Transaction failed: {e}")

def get_key(redis_client, key):
    """Get a value by key from Redis."""
    value = redis_client.get(key)
    return json.loads(value) if value else None

def test_distributed_transactions():
    """Test distributed transactions in Redis."""
    logging.info("Starting the Redis container for distributed transactions testing...")
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

        # Perform a distributed transaction
        perform_transaction(redis_client)

        # Retrieve the results
        value1 = get_key(redis_client, 'transaction_key1')
        value2 = get_key(redis_client, 'transaction_key2')
        counter = redis_client.get('transaction_counter')

        logging.info(f"Transaction key1 value: {value1}")
        logging.info(f"Transaction key2 value: {value2}")
        logging.info(f"Transaction counter value: {counter}")

if __name__ == "__main__":
    test_distributed_transactions()
