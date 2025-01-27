"""
05_field_constraints_and_indexes.py - Tests Redis Field Constraints & Indexing with Testcontainers.

This test validates:
1. **Unique Key Constraints**: Ensures Redis does not allow accidental overwrites.
2. **Data Type Enforcement**: Ensures Redis enforces correct data structures.
3. **TTL Expiration Policy**: Ensures Redis keys expire as expected.
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


def test_data_type_enforcement(redis_client):
    """
    Tests Redis' ability to store and enforce different data types.

    Steps:
    1. Insert an integer value.
    2. Increment the integer using INCR.
    3. Store and retrieve a list.
    4. Validate data types remain consistent.
    """
    redis_client.set("int_key", 5)  # Store an integer
    redis_client.incr("int_key")  # Increment integer value
    value = redis_client.get("int_key")

    assert value == "6", "⚠️ Data type integrity failed for integers!"

    redis_client.lpush("list_key", "item1", "item2")  # Store a list
    list_values = redis_client.lrange("list_key", 0, -1)

    assert list_values == ["item2", "item1"], "⚠️ List storage integrity failed!"

    print("\n✅ Data type enforcement test passed!")


def test_ttl_expiration(redis_client):
    """
    Tests Redis' TTL (Time-To-Live) expiration mechanism.

    Steps:
    1. Insert a key with an expiration time of 3 seconds.
    2. Wait for 4 seconds to ensure expiration.
    3. Attempt to retrieve the expired key.
    4. Validate that the key no longer exists.
    """
    redis_client.setex("ttl_key", 3, "Temporary Data")

    time.sleep(4)  # Allow key to expire

    expired_value = redis_client.get("ttl_key")
    assert expired_value is None, "⚠️ Expired key still exists!"

    print("\n✅ TTL expiration test passed!")
