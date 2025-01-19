import json
import time
import redis
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def register_guest(redis_client, guest_data):
    try:
        # Send guest registration message to Redis
        redis_client.rpush('guest_registration', json.dumps(guest_data))
        logging.info(f"Guest registration message sent: {guest_data}")
    except Exception as e:
        logging.error(f"Error sending guest registration message: {e}")

def handle_guest_registration(redis_client, message_limit=5):
    processed_count = 0  # Counter for processed messages
    while processed_count < message_limit:
        try:
            # Wait for a message from the Redis list
            message = redis_client.blpop('guest_registration', timeout=5)
            if message:
                guest_data = json.loads(message[1])
                logging.info(f"Processing guest registration: {guest_data}")
                # Simulate processing time
                time.sleep(1)
                logging.info(f"Guest registered successfully: {guest_data['name']}")
                processed_count += 1  # Increment the processed count
            else:
                logging.info("No more messages to process.")
                break  # Exit if no messages are available
        except Exception as e:
            logging.error(f"Error processing guest registration: {e}")
            break  # Exit the loop on error

# Test cases
def test_register_guest(redis_container):
    guest = {
        "name": "Aarav Sharma",
        "email": "aarav.sharma@example.com",
        "room_number": 102
    }
    register_guest(redis_container, guest)
    # Check if the guest registration message is in the Redis list
    assert redis_container.llen('guest_registration') == 1

def test_handle_guest_registration(redis_container):
    # Clear the Redis list before the test
    redis_container.delete('guest_registration')

    guest = {
        "name": "Vivaan Gupta",
        "email": "vivaan.gupta@example.com",
        "room_number": 103
    }
    register_guest(redis_container, guest)
    handle_guest_registration(redis_container, message_limit=1)  # Process only 1 message
    # Check if the guest registration message has been processed
    assert redis_container.llen('guest_registration') == 0  # Expecting 0 after processing

def test_multiple_guest_registrations(redis_container):
    # Clear the Redis list before the test
    redis_container.delete('guest_registration')

    guests = [
        {"name": "Reyansh Patel", "email": "reyansh.patel@example.com", "room_number": 104},
        {"name": "Anaya Verma", "email": "anaya.verma@example.com", "room_number": 105},
        {"name": "Ishaan Mehta", "email": "ishaan.mehta@example.com", "room_number": 106}
    ]
    for guest in guests:
        register_guest(redis_container, guest)

    # Check if the guest registration messages are in the Redis list
    assert redis_container.llen('guest_registration') == len(guests)  # Expecting 3
    handle_guest_registration(redis_container, message_limit=len(guests))  # Process all messages
    # Check if all messages have been processed
    assert redis_container.llen('guest_registration') == 0  # Expecting 0 after processing

if __name__ == "__main__":
    # Example guest data
    guest = {
        "name": "Ishaan Mehta",
        "email": "ishaan.mehta@example.com",
        "room_number": 101
    }

    register_guest(redis_container, guest)
    handle_guest_registration(redis_container, message_limit=1)  # Process only 1 message
