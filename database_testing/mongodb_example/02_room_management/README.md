# Example 2: Room Management (MongoDB)

This example demonstrates how to use Testcontainers to test room management operations in a MongoDB database. It covers:

- Setting up a MongoDB container for room management.
- Creating and managing room collections.
- Testing room availability and status updates.
- Implementing room type categorization.

---

## Overview

The test simulates a hotel room management system. It creates a `rooms` collection and performs operations such as:

1. **Room Creation**: Add new rooms with different types and rates.
2. **Room Status**: Track room availability (`available`, `occupied`, `maintenance`).
3. **Room Updates**: Modify room details and status.
4. **Room Queries**: Search and filter rooms by type and status.

---

## Features

### MongoDB Container

- Uses `MongoDbContainer` for an isolated testing environment.
- Implements room-specific database operations.

### Room Management

- Room type categorization (Standard, Deluxe, Suite).
- Room status tracking.
- Rate management.
- Room availability checks.

### Data Validation

- Ensures room data integrity.
- Validates room status transitions.
- Verifies rate calculations.

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
python -m pytest 02_room_management.py -v -s
```

or

```bash
python3 -m pytest 02_room_management.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/fbc7ed18-fbc8-4e0a-a9e9-c337034e7196)

---

## Code Walkthrough

### 1. Room Schema

```python
room = {
    "room_number": "101",
    "room_type": "Standard",
    "rate": 100.00,
    "status": "available",
    "floor": 1,
    "amenities": ["TV", "WiFi", "Air Conditioning"]
}
```

### 2. Room Operations

- **Creation**: Add new rooms with details.
- **Status Updates**: Change room availability.
- **Queries**: Find rooms by type/status.
- **Rate Management**: Update room rates.

### 3. Test Cases

- Room creation validation.
- Status update verification.
- Availability filtering.
- Room type categorization.
- Rate modification checks.

---

## Key Takeaways

### MongoDB Benefits

- Flexible schema for room attributes.
- Efficient querying capabilities.
- Easy status tracking.

### Testing Practices

- Isolated test environment.
- Comprehensive validation.
- Clear test organization.

### Room Management

- Structured room categorization.
- Status transition handling.
- Rate management system.

---

