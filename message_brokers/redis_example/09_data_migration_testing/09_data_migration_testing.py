import json
import redis
import logging
from testcontainers.core.container import DockerContainer
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def migrate_data(source_client, target_client):
    """Migrate data from source Redis to target Redis."""
    keys = source_client.keys('*')
    for key in keys:
        value = source_client.get(key)
        target_client.set(key, value)
        logging.info(f"Migrated key: {key.decode('utf-8')}")

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

def test_data_migration():
    """Test data migration between Redis instances."""
    logging.info("Starting the Redis containers for data migration testing...")
    with DockerContainer("custom-redis-image:latest") as source_container, \
         DockerContainer("custom-redis-image:latest") as target_container:

        source_container.with_exposed_ports(6379)
        target_container.with_exposed_ports(6379)

        source_container.start()
        target_container.start()

        source_host = source_container.get_container_host_ip()
        source_port = source_container.get_exposed_port(6379)

        target_host = target_container.get_container_host_ip()
        target_port = target_container.get_exposed_port(6379)

        source_client = redis.Redis(host=source_host, port=source_port)
        target_client = redis.Redis(host=target_host, port=target_port)

        logging.info("Waiting for Redis to be ready...")
        if not wait_for_redis(source_client) or not wait_for_redis(target_client):
            source_logs = source_container.get_logs()
            target_logs = target_container.get_logs()
            logging.error(f"Source Redis logs:\n{source_logs.decode('utf-8')}")
            logging.error(f"Target Redis logs:\n{target_logs.decode('utf-8')}")
            raise Exception("Redis containers did not start in time.")

        # Add some data to the source Redis
        source_client.set('key1', json.dumps({'name': 'Alice'}))
        source_client.set('key2', json.dumps({'name': 'Bob'}))

        # Migrate data
        migrate_data(source_client, target_client)

        # Verify migration
        for key in ['key1', 'key2']:
            value = target_client.get(key)
            logging.info(f"Retrieved from target Redis: {key} -> {value.decode('utf-8')}")

if __name__ == "__main__":
    test_data_migration()
