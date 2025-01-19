# Example 4: Occupancy Report (MySQL)

This example demonstrates how to test occupancy report generation using Testcontainers and MySQL. It includes:

- Creating `rooms` and `bookings` tables.
- Performing CRUD operations on the tables.
- Generating and validating occupancy reports.

---

## Features

- **MySQL Container**:
  - Uses a custom MySQL container to spin up a database for testing.
  - Automatically handles container lifecycle.

- **Database Operations**:
  - Creates `rooms` and `bookings` tables.
  - Performs CRUD operations and validates the results.

- **Assertions**:
  - Ensures the database operations produce the expected results.

---

## Directory Structure

The directory structure for this example is as follows:
```
mysql_example/
└── 04_occupancy_report/
    ├── 04_occupancy_report.py
    ├── conftest.py
    └── README.md
```

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers sqlalchemy mysql-connector-python
```
or
```bash
pip3 install pytest testcontainers sqlalchemy mysql-connector-python
```
### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 04_occupancy_report.py -v -s
```
or
```bash
python3 -m pytest 04_occupancy_report.py -v -s
```
---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/17632fdc-9d44-4691-a917-2e4eef6718c0)


---

## Code Walkthrough

### 1. `04_occupancy_report.py`
This file contains the test suite for occupancy reports. It includes:

- A custom `MySQLContainer` class to manage the MySQL container.
- Functions to set up the database schema and insert sample data.
- A test function to generate and validate occupancy reports.

### 2. `conftest.py`
This file registers the `occupancy_report` marker for pytest. It allows you to organize and run tests related to occupancy reports.

---

## Key Takeaways

- **Testcontainers**:
  - Simplifies testing by providing lightweight, disposable database containers.

- **SQLAlchemy**:
  - Provides a powerful ORM for interacting with the database.

- **Occupancy Reports**:
  - Demonstrates how to calculate daily occupancy rates, room type availability, and revenue.

- **Assertions**:
  - Ensures the database behaves as expected.

---

## Common Issues

- **Docker Not Running**:
  - Ensure Docker is installed and running on your system.

- **Port Conflicts**:
  - If the MySQL container fails to start, check for port conflicts on your system.

- **Missing Dependencies**:
  - Ensure all required Python packages are installed.

---

## Future Enhancements

- Add more complex queries, such as filtering bookings by date range or room type.
- Test concurrent bookings to simulate real-world scenarios.
- Integrate with a frontend or API layer for end-to-end testing.

---
