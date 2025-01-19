import json
import time
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REDIS_LIST = 'reservations'

def add_reservation(redis_client, reservation_data):
    """Add a reservation to Redis."""
    try:
        # Send reservation message to Redis
        redis_client.rpush(REDIS_LIST, json.dumps(reservation_data))
        logging.info(f"Reservation added: {reservation_data}")
    except Exception as e:
        logging.error(f"Error adding reservation: {e}")

def process_reservations(redis_client, message_limit=5):
    """Process reservations from Redis."""
    processed_count = 0  # Counter for processed messages
    while processed_count < message_limit:
        try:
            # Wait for a message from the Redis list
            message = redis_client.blpop(REDIS_LIST, timeout=5)
            if message:
                reservation_data = json.loads(message[1])
                logging.info(f"Processing reservation: {reservation_data}")
                # Simulate processing time
                time.sleep(1)
                logging.info(f"Reservation processed successfully: {reservation_data['name']}")
                processed_count += 1  # Increment the processed count
            else:
                logging.info("No more reservations to process.")
                break  # Exit if no messages are available
        except Exception as e:
            logging.error(f"Error processing reservation: {e}")
            break  # Exit the loop on error

# Test cases
def test_add_reservation(redis_container):
    """Test adding a reservation."""
    reservation = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "room_number": 201,
        "check_in": "2024-01-01",
        "check_out": "2024-01-05"
    }
    add_reservation(redis_container, reservation)
    # Check if the reservation message is in the Redis list
    assert redis_container.llen(REDIS_LIST) == 1  # Expecting 1 reservation

def test_process_reservations(redis_container):
    """Test processing reservations."""
    # Clear the Redis list before the test
    redis_container.delete(REDIS_LIST)

    reservation = {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "room_number": 202,
        "check_in": "2024-01-10",
        "check_out": "2024-01-15"
    }
    add_reservation(redis_container, reservation)
    process_reservations(redis_container, message_limit=1)  # Process only 1 reservation
    # Check if the reservation message has been processed
    assert redis_container.llen(REDIS_LIST) == 0  # Expecting 0 after processing

def test_multiple_reservations(redis_container):
    """Test handling multiple reservations."""
    # Clear the Redis list before the test
    redis_container.delete(REDIS_LIST)

    reservations = [
        {"name": "Alice Johnson", "email": "alice.johnson@example.com", "room_number": 203, "check_in": "2024-01-20", "check_out": "2024-01-25"},
        {"name": "Bob Brown", "email": "bob.brown@example.com", "room_number": 204, "check_in": "2024-01-22", "check_out": "2024-01-27"},
        {"name": "Charlie Davis", "email": "charlie.davis@example.com", "room_number": 205, "check_in": "2024-01-24", "check_out": "2024-01-29"}
    ]
    for reservation in reservations:
        add_reservation(redis_container, reservation)

    # Check if the reservation messages are in the Redis list
    assert redis_container.llen(REDIS_LIST) == len(reservations)  # Expecting 3
    process_reservations(redis_container, message_limit=len(reservations))  # Process all messages
    # Check if all messages have been processed
    assert redis_container.llen(REDIS_LIST) == 0  # Expecting 0 after processing

if __name__ == "__main__":
    # Example reservation data
    reservation = {
        "name": "David Wilson",
        "email": "david.wilson@example.com",
        "room_number": 206,
        "check_in": "2024-01-30",
        "check_out": "2024-02-05"
    }

    # Initialize Redis client (assuming redis_container is available)
    redis_client = redis.Redis(host='localhost', port=6379)  # Adjust as necessary for your setup
    add_reservation(redis_client, reservation)
    process_reservations(redis_client, message_limit=1)  # Process only 1 reservation
