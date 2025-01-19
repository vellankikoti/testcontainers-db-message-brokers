"""
Multiple Containers Test Suite

This module tests scenarios involving multiple containers, including:
- Setting up a PostgreSQL database and a Redis cache
- Testing interactions between the database and cache
- Verifying data consistency across services
"""

import pytest
import redis
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from sqlalchemy import create_engine, text


def setup_database(connection):
    """Initialize the database schema."""
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    """))
    connection.commit()
    print("✅ Database schema initialized!")


def insert_sample_data(connection):
    """Insert sample data into the database."""
    connection.execute(text("""
        INSERT INTO users (username, email) VALUES
        ('alice', 'alice@example.com'),
        ('bob', 'bob@example.com'),
        ('charlie', 'charlie@example.com');
    """))
    connection.commit()
    print("✅ Sample data inserted into the database!")


def cache_user_data(redis_client, connection):
    """Cache user data from the database into Redis."""
    result = connection.execute(text("SELECT user_id, username, email FROM users;")).fetchall()
    for row in result:
        user_id, username, email = row
        redis_client.hset(f"user:{user_id}", mapping={
            "username": username,
            "email": email
        })
    print("✅ User data cached in Redis!")


def verify_cache(redis_client):
    """Verify that the cached data is correct."""
    keys = redis_client.keys("user:*")
    assert len(keys) == 3, f"Expected 3 users in the cache, found {len(keys)}"

    for key in keys:
        user_data = redis_client.hgetall(key)
        print(f"Cached data for {key}: {user_data}")
        assert "username" in user_data and "email" in user_data, \
            f"Missing data in cache for {key}"

    print("✅ Cache verification successful!")


@pytest.mark.multiple_containers
def test_multiple_containers():
    """Test interactions between multiple containers."""
    # Start both PostgreSQL and Redis containers
    with PostgresContainer("postgres:15.3") as postgres, \
         RedisContainer("redis:7.0") as redis_container:

        # Set up PostgreSQL connection
        postgres_engine = create_engine(postgres.get_connection_url())
        with postgres_engine.connect() as connection:
            setup_database(connection)
            insert_sample_data(connection)

        # Set up Redis connection
        redis_client = redis.StrictRedis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Cache user data from PostgreSQL to Redis
        with postgres_engine.connect() as connection:
            cache_user_data(redis_client, connection)

        # Verify the cached data
        verify_cache(redis_client)

        print("✅ Multiple containers test passed successfully!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
