import json
import logging
from unittest import mock
import redis

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_data(redis_client, key, value):
    """Add data to Redis."""
    redis_client.set(key, json.dumps(value))
    logging.info(f"Added {key}: {value}")

def get_data(redis_client, key):
    """Get data from Redis."""
    value = redis_client.get(key)
    return json.loads(value) if value else None

def test_add_and_get_data():
    """Test adding and getting data using mock Redis client."""
    # Create a mock Redis client
    mock_redis_client = mock.Mock()

    # Define the behavior of the mock client
    mock_redis_client.get.return_value = json.dumps({'name': 'Alice'})

    # Test adding data
    add_data(mock_redis_client, 'key1', {'name': 'Alice'})
    mock_redis_client.set.assert_called_once_with('key1', json.dumps({'name': 'Alice'}))

    # Test getting data
    result = get_data(mock_redis_client, 'key1')
    logging.info(f"Retrieved data: {result}")

    # Verify that the get method was called
    mock_redis_client.get.assert_called_once_with('key1')
    assert result == {'name': 'Alice'}, "The retrieved data does not match the expected value."

if __name__ == "__main__":
    test_add_and_get_data()
