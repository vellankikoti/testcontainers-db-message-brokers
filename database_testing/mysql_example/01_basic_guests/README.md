# Example 1: Basic Guests (MySQL)

## Example 1: Basic Guests (MySQL)
This example demonstrates how to use Testcontainers to test basic MySQL database operations. It covers the following:

- Setting up a MySQL container.
- Creating a database schema.
- Performing basic CRUD (Create, Read, Update, Delete) operations.
- Using assertions to validate the operations.

---

## Overview
The test simulates a simple hotel guest management system. It creates a `guests` table, inserts sample data, and performs the following operations:

- **Insert**: Add guest records to the database.
- **Select**: Retrieve and count the number of guests.
- **Update**: Modify a guest's phone number.
- **Delete**: Remove a guest record.

The test ensures that all operations are performed correctly and validates the results using assertions.

---

## Features

### **MySQL Container**
- Uses the `MySQLContainer` class from the `testcontainers` library to spin up a MySQL database in a Docker container.
- Automatically handles container lifecycle (start and stop).

### **Database Operations**
- Creates a `guests` table with fields for guest details (e.g., name, email, phone).
- Performs CRUD operations and validates the results.

### **Assertions**
- Ensures the database operations produce the expected results.

---

## How to Run the Test

### **1. Install Dependencies**
Install the required Python packages using `pip` or `pip3`:
```bash
pip install pytest testcontainers sqlalchemy mysql-connector-python
```
or
```bash
pip3 install pytest testcontainers sqlalchemy mysql-connector-python
```

### **2. Run the Test**
Execute the test file using `pytest`:
```bash
python -m pytest 01_basic_guests.py -v -s
```
or
```bash
python3 -m pytest 01_basic_guests.py -v -s
```

---

## Expected Output
When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/e137f71c-4a11-4270-8d42-d4ae8bbc5b2f)


---

## Code Walkthrough

### **1. MySQL Container Setup**
The test uses the `MySQLContainer` class to start a MySQL database in a Docker container:
```python
with MySQLContainer("mysql:8.0") as mysql:
    engine = create_engine(mysql.get_connection_url())
```
- The container runs MySQL version 8.0.
- The `get_connection_url()` method provides the connection string for SQLAlchemy.

### **2. Database Schema**
The `setup_database` function creates a `guests` table:
```sql
CREATE TABLE IF NOT EXISTS guests (
    guest_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);
```

### **3. CRUD Operations**
- **Insert**: Adds two guest records to the table.
- **Select**: Counts the number of guests in the table.
- **Update**: Updates the phone number of a guest.
- **Delete**: Deletes a guest record.

### **4. Assertions**
The test uses assertions to validate the results of each operation:
```python
assert count == 2, f"Expected 2 guests, but found {count}"
assert phone == '555-0123', f"Expected updated phone '555-0123', but found {phone}"
```

---

## Key Takeaways

### **Testcontainers**
- Simplifies testing by providing lightweight, disposable database containers.
- Automatically manages container lifecycle.

### **SQLAlchemy**
- Provides a powerful and flexible ORM for interacting with the database.

### **CRUD Operations**
- Demonstrates how to perform and validate basic database operations.

### **Assertions**
- Ensures the database behaves as expected.

---

