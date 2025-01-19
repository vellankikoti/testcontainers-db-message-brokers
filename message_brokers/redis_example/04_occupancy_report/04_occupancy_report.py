import json
import redis
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

REDIS_LIST = "reservations"


def generate_occupancy_report(redis_client):
    """Generate an occupancy report from the reservations in Redis."""
    try:
        reservations = redis_client.lrange(REDIS_LIST, 0, -1)  # Get all reservations
        occupancy = {}

        for reservation in reservations:
            reservation_data = json.loads(reservation)
            room_number = reservation_data["room_number"]
            check_in = datetime.strptime(reservation_data["check_in"], "%Y-%m-%d")
            check_out = datetime.strptime(reservation_data["check_out"], "%Y-%m-%d")

            # Calculate occupied days
            occupied_days = (check_out - check_in).days

            # Populate the occupancy report
            if room_number not in occupancy:
                occupancy[room_number] = {
                    "total_reservations": 0,
                    "occupied_days": 0,
                    "reservations": [],
                }

            occupancy[room_number]["total_reservations"] += 1
            occupancy[room_number]["occupied_days"] += occupied_days
            occupancy[room_number]["reservations"].append(reservation_data)

        # Logging the occupancy report
        logging.info("Occupancy Report Generated:")
        for room, data in occupancy.items():
            logging.info(f"Room {room}:")
            logging.info(f"  Total Reservations: {data['total_reservations']}")
            logging.info(f"  Total Occupied Days: {data['occupied_days']}")
            logging.info(f"  Reservations Details: {data['reservations']}")
            logging.info("")  # Add a blank line for better readability

        return occupancy

    except Exception as e:
        logging.error(f"Error generating occupancy report: {e}")
        return None


def test_generate_occupancy_report(redis_container):
    """Test generating an occupancy report with various scenarios."""
    redis_container.delete(REDIS_LIST)  # Clear Redis list before testing

    # Test Case 1: Basic occupancy report
    reservations = [
        {"name": "John Doe", "email": "john.doe@example.com", "room_number": 101, "check_in": "2024-01-01", "check_out": "2024-01-05"},  # 4 days
        {"name": "Jane Smith", "email": "jane.smith@example.com", "room_number": 101, "check_in": "2024-01-06", "check_out": "2024-01-10"},  # 4 days
        {"name": "David Wilson", "email": "david.wilson@example.com", "room_number": 102, "check_in": "2024-01-01", "check_out": "2024-01-03"},  # 2 days
        {"name": "Alice Johnson", "email": "alice.johnson@example.com", "room_number": 102, "check_in": "2024-01-04", "check_out": "2024-01-07"},  # 3 days
    ]

    for reservation in reservations:
        redis_container.rpush(REDIS_LIST, json.dumps(reservation))

    report = generate_occupancy_report(redis_container)

    assert report is not None
    assert report[101]["total_reservations"] == 2
    assert report[101]["occupied_days"] == 8
    assert report[102]["total_reservations"] == 2
    assert report[102]["occupied_days"] == 5

    # Test Case 2: No reservations
    redis_container.delete(REDIS_LIST)
    report = generate_occupancy_report(redis_container)
    assert report == {}

    # Test Case 3: Single reservation
    single_reservation = {
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "room_number": 103,
        "check_in": "2024-01-10",
        "check_out": "2024-01-12",
    }
    redis_container.rpush(REDIS_LIST, json.dumps(single_reservation))
    report = generate_occupancy_report(redis_container)
    assert report[103]["total_reservations"] == 1
    assert report[103]["occupied_days"] == 2

    # Test Case 4: Overlapping reservations
    overlapping_reservations = [
        {"name": "Eve Adams", "email": "eve.adams@example.com", "room_number": 104, "check_in": "2024-01-01", "check_out": "2024-01-04"},  # 3 days
        {"name": "Bob Marley", "email": "bob.marley@example.com", "room_number": 104, "check_in": "2024-01-03", "check_out": "2024-01-06"},  # 3 days
    ]
    redis_container.rpush(REDIS_LIST, *[json.dumps(r) for r in overlapping_reservations])
    report = generate_occupancy_report(redis_container)
    assert report[104]["total_reservations"] == 2
    assert report[104]["occupied_days"] == 6  # 3 + 3 = 6 days


if __name__ == "__main__":
    # Initialize Redis client (adjust host/port for your setup)
    redis_client = redis.Redis(host="localhost", port=6379)

    # Generate occupancy report
    occupancy_report = generate_occupancy_report(redis_client)
    if occupancy_report:
        logging.info("Occupancy report generated successfully.")
    else:
        logging.error("Failed to generate occupancy report.")
