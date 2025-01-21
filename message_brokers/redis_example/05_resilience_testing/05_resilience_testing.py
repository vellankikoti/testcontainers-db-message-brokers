import json
import redis
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_LIST = 'extended_stays'

def add_extended_stay(redis_client, stay):
    """Add an extended stay to Redis."""
    redis_client.rpush(REDIS_LIST, json.dumps(stay))
    logging.info(f"Added extended stay: {stay}")

def view_extended_stays(redis_client):
    """View all extended stays in Redis."""
    stays = redis_client.lrange(REDIS_LIST, 0, -1)
    return [json.loads(stay) for stay in stays]

def update_extended_stay(redis_client, stay_id, additional_days):
    """Update the duration of an extended stay by adding additional days."""
    stays = view_extended_stays(redis_client)
    for stay in stays:
        if stay['id'] == stay_id:
            stay['check_out'] = (datetime.strptime(stay['check_out'], "%Y-%m-%d") + timedelta(days=additional_days)).strftime("%Y-%m-%d")
            redis_client.lset(REDIS_LIST, stays.index(stay), json.dumps(stay))
            logging.info(f"Updated extended stay: {stay}")
            return True
    logging.warning(f"Extended stay with ID {stay_id} not found.")
    return False

# Test cases
def test_extended_stays(redis_container):
    """Test the extended stays functionality."""
    redis_client = redis_container

    # Clear the Redis list before the test
    redis_client.delete(REDIS_LIST)

    # Test Case 1: Add an extended stay
    stay = {
        "id": 1,
        "guest_name": "John Doe",
        "room_number": 101,
        "check_in": "2024-01-01",
        "check_out": "2024-01-10"
    }
    add_extended_stay(redis_client, stay)
    assert len(view_extended_stays(redis_client)) == 1  # Should have 1 extended stay

    # Test Case 2: View extended stays
    stays = view_extended_stays(redis_client)
    assert len(stays) == 1
    assert stays[0]['id'] == 1  # Check if the stay ID matches

    # Test Case 3: Update an extended stay
    assert update_extended_stay(redis_client, 1, 5)  # Extend by 5 days
    updated_stays = view_extended_stays(redis_client)
    assert updated_stays[0]['check_out'] == "2024-01-15"  # Check if the check-out date is updated

    # Test Case 4: Attempt to update a non-existent extended stay
    assert not update_extended_stay(redis_client, 2, 3)  # Should return False

if __name__ == "__main__":
    # Initialize Redis client (assuming redis_container is available)
    redis_client = redis.Redis(host='localhost', port=6379)  # Adjust as necessary for your setup

    # Example usage
    add_extended_stay(redis_client, {
        "id": 1,
        "guest_name": "John Doe",
        "room_number": 101,
        "check_in": "2024-01-01",
        "check_out": "2024-01-10"
    })
    logging.info("Current extended stays:")
    logging.info(view_extended_stays(redis_client))
