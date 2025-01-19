# Example 5: Extended Stays

## Overview
This example demonstrates how to handle extended stays in a hotel booking system, including:

- Identifying long-term bookings (7+ days)
- Applying automatic discounts for extended stays
- Generating reports for extended stay bookings
- Testing the discount calculation logic

---

## Features

### Extended Stay Detection
- Automatically identifies bookings longer than 7 days.
- Calculates the total length of stay.
- Filters bookings based on minimum stay duration.

### Automatic Discounts
- **10% discount** applied to stays of 7 days or longer.
- Discount calculation handled at the database level.
- Rounded to 2 decimal places for accuracy.

### Reporting
- Generates detailed reports of extended stays.
- Includes original and discounted prices.
- Shows booking duration and guest information.

---

## Code Structure

### Database Schema
```sql
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_type TEXT NOT NULL,
    rate DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'available'
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    room_id INT NOT NULL,
    guest_name TEXT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    CONSTRAINT valid_dates CHECK (check_out > check_in)
);
```

---

## Key Functions

### `setup_database(connection)`
- Creates necessary tables if they don't exist.
- Sets up constraints and relationships.

### `insert_sample_data(connection)`
- Populates tables with test data.
- Creates bookings of various durations.

### `calculate_extended_stays(connection, min_days=7)`
- Identifies bookings longer than the minimum stay.
- Calculates discounted prices.
- Returns detailed booking information.

---

## Running the Tests

### Prerequisites
- **Python 3.8+**
- **Docker**
- Required packages:
  ```bash
  pip install pytest testcontainers sqlalchemy psycopg2-binary
  ```

### Test Execution
Run the tests using:
```bash
python3 -m pytest 05_extended_stays.py -v
```

---

### Expected Output

![image](https://github.com/user-attachments/assets/b090114b-5833-4666-8468-22d8c11add71)

---

## Key Takeaways

### Database Design
- Use of foreign keys for referential integrity.
- Date validation using `CHECK` constraints.
- Decimal precision for monetary values.

### Business Logic
- Automatic discount application.
- Flexible minimum stay configuration.
- Clear reporting structure.

### Testing Approach
- Isolated test environment using Testcontainers.
- Comprehensive assertions.
- Clear test output with formatted reporting.

---

## Common Use Cases

### Monthly Stays
```python
extended_stays = calculate_extended_stays(connection, min_days=30)
```

### Weekly Stays
```python
extended_stays = calculate_extended_stays(connection, min_days=7)
```

### Custom Duration
```python
extended_stays = calculate_extended_stays(connection, min_days=custom_days)
```

---

## Directory Structure
```
05_extended_stays/
├── 05_extended_stays.py  # Main test file
├── conftest.py           # Pytest configuration
└── README.md             # Documentation (this file)
```

---

## Error Handling
The code includes several safety features:
- **Date validation** to ensure check-out is after check-in.
- **Foreign key constraints** to maintain data integrity.
- **Rounding of monetary values** to prevent floating-point errors.

---

## Future Enhancements

### Tiered Discounts
- Different discount rates based on stay duration.
- Special rates for specific room types.
- Seasonal pricing adjustments.

### Additional Features
- Early check-in/late check-out handling.
- Multiple room bookings.
- Loyalty program integration.

### Reporting Improvements
- Revenue forecasting.
- Occupancy optimization.
- Discount impact analysis.
```
