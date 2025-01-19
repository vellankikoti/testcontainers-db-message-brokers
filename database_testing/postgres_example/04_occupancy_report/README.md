# Example 4: Occupancy Reports

## Overview
This example demonstrates how to generate occupancy reports for the "Happy Hotel" database. It covers the following:
- Creating `rooms` and `bookings` tables (if not already created)
- Inserting sample room and booking data
- Querying and analyzing data to generate occupancy reports
- Verifying the results with assertions

---

## Code Walkthrough

### 1. Starting the PostgreSQL Container
The `PostgresContainer` class from Testcontainers is used to start a temporary PostgreSQL instance. This container is automatically cleaned up after the test.

```python
with PostgresContainer("postgres:15.3") as postgres:
    engine = postgres.get_connection_engine()
```

- **PostgresContainer**: Spins up a PostgreSQL container using the specified image (`postgres:15.3`).
- **get_connection_engine()**: Provides a SQLAlchemy engine to interact with the database.

This ensures a clean and isolated database environment for each test.

---

### 2. Creating the `rooms` and `bookings` Tables
Two tables are created:
1. **`rooms`**: Stores room information, including room type, rate, and availability status.
2. **`bookings`**: Stores booking details, including the room ID, guest name, check-in/check-out dates, and total price.

```sql
CREATE TABLE IF NOT EXISTS rooms (
    room_id SERIAL PRIMARY KEY,
    room_type TEXT NOT NULL,
    rate DECIMAL(10,2) NOT NULL,
    status TEXT DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS bookings (
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

- **FOREIGN KEY**: Establishes a relationship between the `bookings` table and the `rooms` table.
- **CHECK Constraint**: Ensures that the `check_out` date is always after the `check_in` date.

---

### 3. Inserting Sample Data
Sample data is added to both tables to simulate hotel rooms and bookings.

#### Rooms:
```sql
INSERT INTO rooms (room_type, rate) VALUES
('Standard', 100.00),
('Deluxe', 150.00),
('Suite', 250.00),
('Standard', 100.00),
('Deluxe', 150.00);
```

#### Bookings:
```sql
INSERT INTO bookings (room_id, guest_name, check_in, check_out, total_price) VALUES
(1, 'Alice', '2024-12-24', '2024-12-25', 100.00),
(2, 'Bob', '2024-12-24', '2024-12-26', 300.00),
(3, 'Charlie', '2024-12-25', '2024-12-27', 500.00);
```

---

### 4. Generating Occupancy Reports
The `SELECT` SQL command calculates the number of occupied rooms, total rooms, and revenue for each day. It generates a date range and counts overlapping bookings.

```sql
WITH daily_occupancy AS (
    SELECT 
        d.date,
        COUNT(DISTINCT b.room_id) as occupied_rooms,
        COUNT(DISTINCT r.room_id) as total_rooms,
        SUM(CASE 
            WHEN b.room_id IS NOT NULL 
            THEN r.rate 
            ELSE 0 
        END) as daily_revenue
    FROM generate_series('2024-12-24', '2024-12-30', INTERVAL '1 day') as d(date)
    CROSS JOIN rooms r
    LEFT JOIN bookings b ON r.room_id = b.room_id
    AND d.date BETWEEN b.check_in AND b.check_out - 1
    GROUP BY d.date
)
SELECT 
    date,
    occupied_rooms,
    total_rooms,
    ROUND((occupied_rooms::float / total_rooms::float * 100)::numeric, 2) as occupancy_rate,
    daily_revenue
FROM daily_occupancy
ORDER BY date;
```

- **`generate_series`**: Creates a range of dates for the report.
- **LEFT JOIN**: Combines room and booking data, even if no bookings exist for a room.
- **CASE**: Calculates daily revenue based on room rates.

---

### 5. Verifying the Results
Assertions ensure that the occupancy data matches expectations.

```python
assert len(report) == 7, "The report should cover 7 days."
assert report[0].occupancy_rate == 40.0, "Expected 40% occupancy on the first day."
assert report[0].daily_revenue == 200.00, "Expected $200 revenue on the first day."
```

---

## How to Run

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker
- Required Python packages: `pytest`, `testcontainers`, `sqlalchemy`, `psycopg2-binary`

Install the dependencies using `pip`:
```bash
pip install pytest testcontainers sqlalchemy psycopg2-binary
```

### Running All Tests
Run all the tests in the file:
```bash
python3 -m pytest 04_occupancy_report.py -v
```
## Expected Output
Example test output:
![image](https://github.com/user-attachments/assets/df45365b-5554-48f9-a2f1-ea090978ad48)

### Running a Specific Test Case
Run a specific test case using its node ID:
```bash
python3 -m pytest 04_occupancy_report.py::test_occupancy_calculation -v
```

Alternatively, use a marker defined in `conftest.py`:
```bash
python3 -m pytest -m occupancy -v
```

---

## Expected Output
Example test output:
![image](https://github.com/user-attachments/assets/d4bf41fd-0be4-4caa-910b-9d8367b77024)


---

## Key Takeaways
- **Data Analysis**: Demonstrates how to analyze room and booking data to generate reports.
- **SQL Aggregation**: Uses SQL functions like `COUNT`, `SUM`, and `ROUND` for data aggregation.
- **Dynamic Queries**: Shows how to calculate occupancy and revenue for specific dates or ranges.
- **Testcontainers**: Provides a clean, isolated database environment for testing.

---

## Directory Structure
```
04_occupancy_report/
├── 04_occupancy_report.py  # Test code for occupancy reports
├── conftest.py             # Pytest configuration for marker registration
├── README.md               # Documentation (this file)
```
