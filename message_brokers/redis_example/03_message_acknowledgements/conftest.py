"""
conftest.py - Shared fixtures for Redis example
"""

import pytest
from testcontainers.redis import RedisContainer
import redis

@pytest.fixture(scope="module")
def redis_container():
    """Start a Redis container and provide the connection details."""
    with RedisContainer("redis:latest") as redis_server:
        yield redis_server

@pytest.fixture(scope="module")
def redis_client(redis_container):
    """Set up a Redis client."""
    client = redis.Redis(host=redis_container.get_container_host_ip(), port=redis_container.get_exposed_port(6379))
    yield client
    client.close()