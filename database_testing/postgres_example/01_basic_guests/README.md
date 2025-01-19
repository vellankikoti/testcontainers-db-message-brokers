# Example 1: Basic Guest Registration

## Overview

This example demonstrates how to use Testcontainers to test a simple guest registration system. It covers the following:

- Creating a `guests` table
- Inserting sample guest data
- Retrieving and verifying the data

---
**Note:**
Use any of the following command to install the prerequisites
```
pip install pytest testcontainers-python psycopg2-binary sqlalchemy
```
or 
```
pip3 install pytest testcontainers-python psycopg2-binary
```
If you run into any pytest related issue manually install only pytest by any of the following command
```
pip install pytest
```
or
```
pip3 install pytest
```

## Code Walkthrough

### 1. Starting the PostgreSQL Container
The `PostgresContainer` class from Testcontainers is used to start a temporary PostgreSQL instance. This container is automatically cleaned up after the test.

```python
with PostgresContainer(POSTGRES_VERSION) as postgres:
        engine = create_engine(postgres.get_connection_url())
```

- **`PostgresContainer`**: Spins up a PostgreSQL container using the specified image (`postgres:15.3`).
- **`get_connection_url()`**: Provides a SQLAlchemy engine to interact with the database.

---

### 2. Creating the `guests` Table
The `CREATE TABLE` SQL command is used to define a table with two columns:
- `guest_id`: A unique identifier for each guest (auto-incrementing primary key).
- `guest_name`: The name of the guest (text).

```python
# Constants
POSTGRES_VERSION = "postgres:15.3"
CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS guests (
        guest_id SERIAL PRIMARY KEY,
        guest_name TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
```
```python
def setup_database(connection):
    """Set up the database schema."""
    connection.execute(text(CREATE_TABLE_QUERY))
    connection.commit()
```

- **`CREATE TABLE IF NOT EXISTS`**: Ensures the table is created only if it doesn't already exist.
- **`SERIAL`**: Automatically generates unique IDs for each row.

---

### 3. Inserting Guest Data
Two guests, "Alice" and "Bob," are added to the `guests` table using the `INSERT INTO` SQL command.

```python
conn.execute("INSERT INTO guests (guest_name) VALUES ('Alice'), ('Bob');")
```

- **`INSERT INTO`**: Adds new rows to the table.
- **`VALUES`**: Specifies the data to be inserted.

---

### 4. Retrieving and Verifying Data
The `SELECT` SQL command is used to fetch all guest names from the table. The test then verifies that the data matches expectations using assertions.

```python
result = conn.execute("SELECT guest_name FROM guests;")
guest_names = [row[0] for row in result]

assert len(guest_names) == 2, "There should be exactly 2 guests in the database."
assert "Alice" in guest_names, "Alice should be in the guest list."
assert "Bob" in guest_names, "Bob should be in the guest list."
```

- **`SELECT`**: Retrieves data from the table.
- **Assertions**: Ensure the data is correct and matches expectations.

---

## How to Run

Run the test using the following command:

```bash
python -m pytest 01_basic_guests.py -v
```

### Expected Output
When you run the test, you should see the following output:

![image](https://github.com/user-attachments/assets/864d01ce-61e8-44e6-a203-3d42006725d5)

---

## Running Specific Test Cases in Pytest

To run a specific test case in pytest, you can use the `-k` option, directly specify the test function name, or utilize markers.

### 1. Using the Test Function Name

You can directly specify the test file and the test function name in the command. For example:

```bash
python -m pytest 01_basic_guests.py::test_basic_guest_insertion -v
```
or 
```bash
python3 -m pytest 01_basic_guests.py::test_basic_guest_insertion -v
```
### Expected Output

![image](https://github.com/user-attachments/assets/c06098ce-6a54-42d7-b74a-24d3da1c18ba)

This will only run the `test_basic_guest_insertion` test case.

---

### 2. Using the `-k` Option
The `-k` option allows you to run tests that match a specific substring in their name. For example:
```bash
python -m pytest -k "test_basic_guest_insertion" -v
```
or
```bash
python3 -m pytest -k "test_basic_guest_insertion" -v
```
### Expected Output
![image](https://github.com/user-attachments/assets/ba274dd4-5309-4974-a61e-6c7f6c8b7cf3)

---
This will also run the `test_basic_guest_insertion` test case. The `-k` option is useful if you want to run multiple tests that share a common substring in their names.

### 3. Running Tests by Marker

If you want to run all tests with a specific marker (e.g., `@pytest.mark.basic`), you can use the `-m` option. For example:

```bash
python -m pytest -m basic -v
```
or
```bash
python3 -m pytest -m basic -v
```
### Expected Output
![image](https://github.com/user-attachments/assets/8db2ae4b-c45b-4ab1-882c-33218e84678f)

This will run all tests marked with `@pytest.mark.basic`.

### Examples

#### Run only `test_guest_deletion`

```bash
python -m pytest 01_basic_guests.py::test_guest_deletion -v
```
or 
```bash
python3 -m pytest 01_basic_guests.py::test_guest_deletion -v
```
### Expected Output
![image](https://github.com/user-attachments/assets/0b924575-dd98-4613-8188-6cfa474eea96)

---

#### Run all tests that have "update" in their name
```bash
python -m pytest -k "update" -v
```
or
```bash
python3 -m pytest -k "update" -v
```
### Expected Output
![image](https://github.com/user-attachments/assets/28c9df0e-0910-4df9-942e-ce1e16770ce0)

---
### Bonus: Running Tests with Debugging
If you want to debug a specific test case, you can use the `--pdb` option to drop into the Python debugger when a test fails. For example:

```bash
python -m pytest 01_basic_guests.py::test_guest_update --pdb -v
```
or
```bash
python3 -m pytest 01_basic_guests.py::test_guest_update --pdb -v
```
This will run `test_guest_update` and allow you to debug it interactively if it fails.

### Expected Output

![image](https://github.com/user-attachments/assets/7360234b-82bd-42a4-96a0-c8edfb0e12c7)

---


## Key Takeaways

- **Testcontainers**: Automatically starts and stops a PostgreSQL container for the test.
- **Isolation**: Each test runs in a clean environment, ensuring no leftover data.
- **Simplicity**: This example focuses on the basics of database operations.

---
