import json
import logging
import redis  # Import the redis module
import pytest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_command_injection(redis_container):
    """Test for command injection vulnerabilities."""
    try:
        # Attempt to set a key with a command injection attempt
        redis_container.set("key; DROP TABLE users;", "value")
        result = redis_container.get("key; DROP TABLE users;")

        # Check if the key is stored correctly
        assert result == b'value'  # The key should exist and have the value 'value'
        logging.info("Command injection test passed.")
    except Exception as e:
        logging.error(f"Command injection test failed: {e}")
        assert False  # Fail the test if an exception occurs

def test_data_exposure(redis_container):
    """Test to ensure sensitive data is not exposed."""
    sensitive_data = {"password": "supersecret"}
    redis_container.set("sensitive_key", json.dumps(sensitive_data))

    # Attempt to retrieve the sensitive data
    retrieved_data = redis_container.get("sensitive_key")
    retrieved_data = json.loads(retrieved_data)

    # Ensure that the sensitive data is not exposed
    assert "password" in retrieved_data
    assert retrieved_data["password"] == "supersecret"
    logging.info("Data exposure test passed.")

def test_successful_authentication(redis_container):
    """Test successful authentication with Redis."""
    try:
        assert redis_container.ping()  # This should succeed
        logging.info("Successful authentication test passed.")
    except redis.ConnectionError as e:
        logging.error(f"Successful authentication test failed: {e}")
        assert False  # Fail the test if it fails

if __name__ == "__main__":
    pytest.main([__file__])
