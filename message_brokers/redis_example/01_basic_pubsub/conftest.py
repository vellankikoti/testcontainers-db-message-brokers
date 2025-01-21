import pytest
from testcontainers.redis import RedisContainer
import redis

@pytest.fixture(scope='session')
def redis_container():
    """Fixture to start a Redis container and provide a Redis client for tests."""
    # Start a Redis container
    with RedisContainer("redis:latest") as redis_container:
        # Get the host and port for the Redis connection
        host = redis_container.get_container_host_ip()
        port = redis_container.get_exposed_port(6379)

        # Create a Redis client
        client = redis.StrictRedis(host=host, port=port, db=0)

        # Wait for Redis to be ready
        try:
            client.ping()  # This will raise an exception if Redis is not ready
        except redis.ConnectionError:
            pytest.fail("Redis is not ready for connections.")

        yield client  # Yield the Redis client for use in tests

        # Optionally, you can add cleanup code here if needed
