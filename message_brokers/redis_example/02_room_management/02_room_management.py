import json
import time
import redis
import logging
from testcontainers.redis import RedisContainer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_LIST = 'room_management'

def update_room_availability(redis_client, room_id, available):
    """Update the availability of a room in Redis."""
    message = {
        'room_id': room_id,
        'available': available,
        'timestamp': time.time()
    }
    try:
        # Send room availability update message to Redis
        redis_client.rpush(REDIS_LIST, json.dumps(message))
        logging.info(f"Room availability updated: {message}")
    except Exception as e:
        logging.error(f"Error sending room availability message: {e}")

def handle_room_management(redis_client, message_limit=5):
    """Handle room management messages from Redis."""
    processed_count = 0  # Counter for processed messages
    while processed_count < message_limit:
        try:
            # Wait for a message from the Redis list
            message = redis_client.blpop(REDIS_LIST, timeout=5)
            if message:
                room_update = json.loads(message[1])
                logging.info(f"Processing room update: {room_update}")
                # Simulate processing time
                time.sleep(1)
                logging.info(f"Room {room_update['room_id']} availability set to {room_update['available']}")
                processed_count += 1  # Increment the processed count
            else:
                logging.info("No more messages to process.")
                break  # Exit if no messages are available
        except Exception as e:
            logging.error(f"Error processing room management: {e}")
            break  # Exit the loop on error

# Test cases
def test_update_room_availability(redis_container):
    """Test updating room availability."""
    # Use the redis_container directly as the Redis client
    update_room_availability(redis_container, room_id=101, available=True)
    # Check if the room update message is in the Redis list
    assert redis_container.llen(REDIS_LIST) == 1  # Use redis_client to check length

def test_handle_room_management(redis_container):
    """Test handling room management messages."""
    # Clear the Redis list before the test
    redis_container.delete(REDIS_LIST)  # Use redis_client to delete the list

    update_room_availability(redis_container, room_id=102, available=False)
    handle_room_management(redis_container, message_limit=1)  # Process only 1 message
    # Check if the room update message has been processed
    assert redis_container.llen(REDIS_LIST) == 0  # Expecting 0 after processing

def test_multiple_room_updates(redis_container):
    """Test handling multiple room updates."""
    # Clear the Redis list before the test
    redis_container.delete(REDIS_LIST)  # Use redis_client to delete the list

    room_updates = [
        {"room_id": 103, "available": True},
        {"room_id": 104, "available": False},
        {"room_id": 105, "available": True}
    ]
    for update in room_updates:
        update_room_availability(redis_container, **update)

    # Check if the room update messages are in the Redis list
    assert redis_container.llen(REDIS_LIST) == len(room_updates)  # Expecting 3
    handle_room_management(redis_container, message_limit=len(room_updates))  # Process all messages
    # Check if all messages have been processed
    assert redis_container.llen(REDIS_LIST) == 0  # Expecting 0 after processing

if __name__ == "__main__":
    # Example room update data
    room_update = {
        "room_id": 106,
        "available": True
    }

    # Initialize Redis client (assuming redis_container is available)
    redis_client = redis.Redis(host='localhost', port=6379)  # Adjust as necessary for your setup
    update_room_availability(redis_client, **room_update)
    handle_room_management(redis_client, message_limit=1)  # Process only 1 message
