"""
Multiple Containers Testing Example

This script tests the interaction between a MySQL database and a Redis cache.
It ensures data consistency and validates integration between the two services.
"""

import pytest
import time
from sqlalchemy import create_engine, text
from testcontainers.mysql import MySqlContainer
from testcontainers.redis import RedisContainer
import redis

# Constants
MYSQL_VERSION = "mysql:8.0"
REDIS_VERSION = "redis:7.0"
DATABASE_NAME = "integration_test"
MYSQL_ROOT_PASSWORD = "test"

def wait_for_mysql_ready(engine, max_retries=10, retry_interval=2):
    """Wait for the MySQL database to be ready."""
    print("\nWaiting for MySQL to be ready...")
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("MySQL is ready!")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet. Retrying...")
            time.sleep(retry_interval)
    raise RuntimeError("MySQL did not become ready in time.")

@pytest.fixture(scope="module")
def mysql_container():
    """Fixture to provide a MySQL container."""
    with MySqlContainer(MYSQL_VERSION) as container:
        container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        container.with_env("MYSQL_DATABASE", DATABASE_NAME)
        yield container

@pytest.fixture(scope="module")
def redis_container():
    """Fixture to provide a Redis container."""
    with RedisContainer(REDIS_VERSION) as container:
        yield container

@pytest.fixture(scope="module")
def mysql_engine(mysql_container):
    """Fixture to provide a SQLAlchemy engine for MySQL."""
    engine = create_engine(mysql_container.get_connection_url())
    wait_for_mysql_ready(engine)
    setup_database(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def redis_client(redis_container):
    """Fixture to provide a Redis client."""
    client = redis.StrictRedis(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        decode_responses=True
    )
    yield client
    client.close()

def setup_database(engine):
    """Set up the MySQL database schema and insert sample data."""
    print("\nSetting up MySQL database...")
    with engine.connect() as connection:
        # Create a users table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        connection.commit()
        print("Created users table.")

        # Insert sample data
        connection.execute(text("""
            INSERT INTO users (name, email) VALUES
            ('Alice', 'alice@example.com'),
            ('Bob', 'bob@example.com'),
            ('Charlie', 'charlie@example.com');
        """))
        connection.commit()
        print("Inserted sample data.")

def sync_data_to_redis(engine, redis_client):
    """Synchronize data from MySQL to Redis."""
    print("\nSynchronizing data from MySQL to Redis...")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name, email FROM users;"))
        for row in result.mappings():
            user_id = row["id"]
            user_data = {
                "name": row["name"],
                "email": row["email"]
            }
            redis_client.hmset(f"user:{user_id}", user_data)
            print(f"Synchronized user {user_id} to Redis.")

def validate_redis_data(redis_client):
    """Validate data in Redis."""
    print("\nValidating data in Redis...")
    keys = redis_client.keys("user:*")
    assert len(keys) == 3, f"Expected 3 users in Redis, found {len(keys)}."
    for key in keys:
        user_data = redis_client.hgetall(key)
        print(f"Validated Redis data for {key}: {user_data}")
        assert "name" in user_data and "email" in user_data, f"Invalid data for {key}."

@pytest.mark.integration
def test_mysql_to_redis_sync(mysql_engine, redis_client):
    """Test the synchronization of data from MySQL to Redis."""
    sync_data_to_redis(mysql_engine, redis_client)
    validate_redis_data(redis_client)
    print("\nTest completed successfully!")

def run_integration_test():
    """Run the integration test directly."""
    print("\nStarting integration test...")
    try:
        # Start MySQL container
        mysql_container = MySqlContainer(MYSQL_VERSION)
        mysql_container.with_env("MYSQL_ROOT_PASSWORD", MYSQL_ROOT_PASSWORD)
        mysql_container.with_env("MYSQL_DATABASE", DATABASE_NAME)
        mysql_container.start()
        print("MySQL container started.")

        # Start Redis container
        redis_container = RedisContainer(REDIS_VERSION)
        redis_container.start()
        print("Redis container started.")

        # Create MySQL engine
        engine = create_engine(mysql_container.get_connection_url())
        wait_for_mysql_ready(engine)
        setup_database(engine)

        # Create Redis client
        redis_client = redis.StrictRedis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379),
            decode_responses=True
        )

        # Run the test
        sync_data_to_redis(engine, redis_client)
        validate_redis_data(redis_client)

        print("\nTest completed successfully!")

    except Exception as e:
        print(f"\nTest failed: {e}")
        raise
    finally:
        # Cleanup
        print("\nCleaning up...")
        try:
            engine.dispose()
            redis_client.close()
            mysql_container.stop()
            redis_container.stop()
            print("Cleanup completed.")
        except Exception as e:
            print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    run_integration_test()
