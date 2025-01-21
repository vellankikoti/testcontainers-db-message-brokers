"""
03_message_acknowledgements.py - Demonstrates Redis message acknowledgements with Testcontainers.

This example verifies that messages are acknowledged and properly processed in Redis lists.
"""

import pytest
import time

def test_redis_message_acknowledgement(redis_client):
    """Test that messages added to a Redis list are acknowledged and removed after processing."""
    redis_client.rpush("task_queue", "Task 1")
    redis_client.rpush("task_queue", "Task 2")
    
    # Simulate worker processing tasks
    processed_task = redis_client.lpop("task_queue")
    assert processed_task is not None
    assert processed_task.decode("utf-8") == "Task 1"
    
    # Ensure only one task remains
    remaining_tasks = redis_client.llen("task_queue")
    assert remaining_tasks == 1