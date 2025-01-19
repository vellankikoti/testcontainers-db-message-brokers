# Example 5: Extended Stays (MongoDB)

This example demonstrates how to use Testcontainers to test scenarios involving extended stays in a hotel using MongoDB. It covers:

- Managing extended bookings.
- Updating reservation dates.
- Recalculating total costs.
- Handling overlapping reservations.
- Validating extended stay rules.

---

## Overview

The test simulates a hotel reservation system that supports extended stays. It performs the following operations:

1. **Extend Stay**: Modify check-out dates for existing reservations.
2. **Cost Recalculation**: Recalculate the total cost based on the extended duration.
3. **Conflict Handling**: Ensure no overlapping reservations occur.
4. **Validation Rules**: Enforce maximum stay limits and other constraints.

---

## Features

### Extended Stay Management

- Update check-out dates for reservations.
- Recalculate total costs dynamically.
- Validate extended stay rules.

### Conflict Prevention

- Check for overlapping reservations.
- Ensure room availability during the extended period.

### Cost Calculation

- Calculate additional charges for extended stays.
- Apply discounts for long-term stays.

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
python -m pytest 05_extended_stays.py -v -s
```

or

```bash
python3 -m pytest 05_extended_stays.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/ff7fc3a9-43b4-4a50-bc36-bbdc505b148e)


---

## Code Walkthrough

### 1. Reservation Schema

```python
reservation = {
    "reservation_id": "RES002",
    "guest_id": "GUEST002",
    "room_id": "102",
    "check_in": "2024-01-01",
    "check_out": "2024-01-10",
    "status": "confirmed",
    "total_cost": 900.00,
    "created_at": "2024-01-01T10:00:00Z"
}
```

### 2. Key Operations

- Extend reservation dates.
- Recalculate total costs.
- Check for overlapping reservations.
- Validate maximum stay limits.
- Apply discounts for long-term stays.

### 3. Test Cases

- Extend stay validation.
- Cost recalculation for extended stays.
- Overlapping reservation prevention.
- Maximum stay limit enforcement.
- Long-term discount application.

---

## Key Takeaways

### MongoDB Benefits

- Flexible schema for reservation updates.
- Efficient date range queries.
- Easy conflict detection.
- Dynamic cost calculations.

### Testing Practices

- Comprehensive validation.
- Edge case handling.
- Clear test organization.
- Proper cleanup.

### Extended Stay Management

- Robust date handling.
- Dynamic cost adjustments.
- Conflict prevention.
- Rule enforcement.

---
