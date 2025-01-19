# Example 3: Reservations (MongoDB)

This example demonstrates how to use Testcontainers to test a hotel reservation system using MongoDB. It covers:

- Managing room reservations.
- Handling booking dates.
- Implementing reservation status tracking.
- Testing booking conflicts.
- Validating reservation rules.

---

## Overview

The test simulates a hotel reservation system that:

1. Creates and manages reservations.
2. Checks room availability for specific dates.
3. Handles booking conflicts.
4. Manages reservation status changes.
5. Calculates booking costs.

---

## Features

### Reservation Management

- Create new reservations.
- Update reservation status.
- Handle check-in/check-out.
- Process cancellations.

### Date Handling

- Validate booking dates.
- Check availability periods.
- Handle date overlaps.
- Process date modifications.

### Validation Rules

- Prevent double bookings.
- Validate stay duration.
- Check room availability.
- Enforce minimum/maximum stay limits.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 03_reservations.py -v -s
```

or

```bash
python3 -m pytest 03_reservations.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/d48001a5-3504-461c-ac27-0d0e6ce48eaa)

---

## Code Walkthrough

### 1. Reservation Schema

```python
reservation = {
    "reservation_id": "RES001",
    "guest_id": "GUEST001",
    "room_id": "101",
    "check_in": "2024-01-01",
    "check_out": "2024-01-05",
    "status": "confirmed",
    "total_cost": 400.00,
    "created_at": "2024-01-01T10:00:00Z"
}
```

### 2. Key Operations

- Create new reservations.
- Check room availability.
- Update reservation status.
- Calculate booking costs.
- Handle cancellations.

### 3. Test Cases

- Reservation creation.
- Availability checking.
- Double booking prevention.
- Status updates.
- Cancellation processing.
- Cost calculations.

---

## Key Takeaways

### MongoDB Benefits

- Flexible reservation schema.
- Efficient date queries.
- Easy status tracking.
- Transaction support.

### Testing Practices

- Comprehensive validation.
- Edge case handling.
- Clear test organization.
- Proper cleanup.

### Reservation System

- Robust booking logic.
- Status management.
- Cost calculation.
- Conflict prevention.

---


