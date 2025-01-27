"""
conftest.py - Shared fixtures for Redis example.

This file provides:
1. A fixture to start a Redis container.
2. A fixture to establish a Redis client connection.
"""

import pytest
from testcontainers.redis import RedisContainer
import redis
import time

@pytest.fixture(scope="module")
def redis_container():
    """
    Starts a Redis container for testing.

    - Uses the latest Redis Docker image.
    - Exposes the default Redis port (6379).
    - Ensures the container is cleaned up after tests.

    Returns:
        RedisContainer: The running Redis Testcontainer instance.
    """
    with RedisContainer("redis:latest") as redis_server:
        yield redis_server

@pytest.fixture(scope="module")
def redis_client(redis_container):
    """
    Establishes a Redis client connection.

    - Retrieves the container's IP and exposed port.
    - Creates a Redis client instance.
    - Ensures Redis is ready before returning the client.
    - Closes the connection automatically after tests.

    Returns:
        redis.Redis: An active Redis client instance.
    """
    client = redis.Redis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        decode_responses=True  # Ensures Redis returns string values
    )

    # ✅ Explicitly wait until Redis is ready
    for _ in range(10):  # Retry for up to 10 seconds
        try:
            if client.ping():  # Redis responds when fully ready
                print("✅ Redis is ready!")
                break
        except redis.exceptions.ConnectionError:
            print("⏳ Waiting for Redis to be ready...")
            time.sleep(1)
    else:
        raise RuntimeError("❌ Redis did not start in time!")

    yield client
    client.close()
