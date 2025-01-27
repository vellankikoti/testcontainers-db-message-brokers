"""
03_data_integrity_testing.py - Tests Redis Data Integrity using Testcontainers.

This test validates:
1. **Unique Key Constraints**: Ensures that duplicate keys cannot overwrite existing values.
2. **Data Retrieval Integrity**: Ensures data consistency after insertions.
3. **Expiration Policy**: Ensures data expires as expected when TTL is set.

The test uses a disposable Redis instance provided by Testcontainers.
"""

import pytest
import time

def test_unique_key_constraint(redis_client):
    """
    Tests Redis' ability to enforce unique key constraints using SETNX.

    Steps:
    1. Insert a key using SETNX (Set if Not Exists).
    2. Attempt to overwrite the same key using SETNX.
    3. Validate that the second insertion fails.
    """
    result1 = redis_client.setnx("unique_key", "First Value")  # Should succeed
    result2 = redis_client.setnx("unique_key", "Duplicate Value")  # Should fail

    assert result1 == 1, "⚠️ Unique key insertion failed!"
    assert result2 == 0, "⚠️ Duplicate key was allowed!"

    print("\n✅ Unique key constraint test passed!")


def test_data_retrieval_integrity(redis_client):
    """
    Tests if Redis correctly retrieves inserted data.

    Steps:
    1. Insert a key-value pair.
    2. Retrieve the value from Redis.
    3. Validate that the retrieved value matches the original.
    """
    redis_client.set("data_key", "Redis Integrity Test")
    retrieved_value = redis_client.get("data_key")

    assert retrieved_value == "Redis Integrity Test", "⚠️ Data integrity mismatch!"

    print("\n✅ Data retrieval integrity test passed!")


def test_expiration_policy(redis_client):
    """
    Tests Redis' TTL (Time-To-Live) expiration mechanism.

    Steps:
    1. Insert a key with an expiration time of 2 seconds.
    2. Wait for 3 seconds to ensure expiration.
    3. Attempt to retrieve the expired key.
    4. Validate that the key no longer exists.
    """
    redis_client.setex("temp_key", 2, "Temporary Data")

    time.sleep(3)  # Allow key to expire

    expired_value = redis_client.get("temp_key")
    assert expired_value is None, "⚠️ Expired key still exists!"

    print("\n✅ Expiration policy test passed!")

