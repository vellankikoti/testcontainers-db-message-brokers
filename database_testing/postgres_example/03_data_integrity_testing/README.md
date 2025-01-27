# Example 3: Data Integrity Testing (PostgreSQL)

This example demonstrates how to use **Testcontainers** to test **data integrity in PostgreSQL**. It ensures that:
- **Unique constraints** prevent duplicate records.
- **Transactions maintain atomicity** (all or nothing).
- **Foreign key constraints** enforce referential integrity.

---

## **Overview**

The test simulates **real-world data validation scenarios** using PostgreSQL. It performs the following operations:

1. **Unique Constraint Enforcement**: Ensures that duplicate records are not allowed in the database.
2. **Transaction Atomicity**: Verifies that failed transactions roll back correctly.
3. **Foreign Key Constraints**: Ensures that child records cannot exist without a valid parent.

Each operation is validated using **assertions** to ensure expected results.

---

## **Features**

### **PostgreSQL Container**
- Uses **Testcontainers** to create a **temporary, isolated PostgreSQL database**.
- Automatically **starts and stops the container** before and after tests.

### **Data Integrity Checks**
- **Unique Constraint**: Ensures duplicate emails cannot be inserted.
- **Transaction Atomicity**: Ensures that **partial updates are not committed** if an error occurs.
- **Foreign Key Constraints**: Prevents inserting orphaned records.

### **Assertions**
- **Prevents duplicate records**.
- **Ensures transaction rollback on failure**.
- **Verifies foreign key constraints are enforced**.

---

## **How to Run the Test**

### **1. Install Dependencies**
Ensure you have all required dependencies installed:

#### **Using `pip`**
```bash
pip install pytest testcontainers psycopg2-binary
```

#### **Using `pip3`**
```bash
pip3 install pytest testcontainers psycopg2-binary
```

### **2. Run the Test**
Execute the test using `pytest`:

#### **Using Python 2/Windows**
```bash
python -m pytest 03_data_integrity_testing.py -v -s
```

#### **Using Python 3/Linux/macOS**
```bash
python3 -m pytest 03_data_integrity_testing.py -v -s
```

---

## **Expected Output**
When you run the test, you should see output similar to this:

![image](https://github.com/user-attachments/assets/9ffa7914-43b0-484f-9bb1-fd689a31780c)

---

If the test fails, possible errors might be:
- **Unique Constraint Failed** (Duplicate was allowed).
- **Transaction Atomicity Failed** (Partial commit was allowed).
- **Foreign Key Constraint Failed** (Orphaned record was inserted).

---

## **Code Walkthrough**

### **1. PostgreSQL Container Setup**
The test uses **Testcontainers** to start a PostgreSQL instance inside a Docker container:

```python
with PostgresContainer("postgres:latest") as postgres:
    yield postgres.get_connection_url()
```

- The container runs **PostgreSQL latest version**.
- The `get_connection_url()` method provides the **PostgreSQL connection string**.

### **2. Database Connection**
The `postgres_cursor` fixture initializes a **test database connection**:

```python
connection = psycopg2.connect(
    host=postgres_container.get_container_host_ip(),
    port=postgres_container.get_exposed_port(5432),
    user="test",
    password="test",
    dbname="test"
)
cursor = connection.cursor()
```

- The **test database** is created automatically.
- The **cursor is used to execute SQL queries**.

### **3. Data Integrity Tests**
#### **a) Unique Constraint Enforcement**
- **Creates a table with a `UNIQUE` constraint on `email`**.
- **Attempts duplicate inserts** and ensures failure.

```python
postgres_cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, name VARCHAR(100) NOT NULL)")
postgres_cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", ("alice@example.com", "Alice"))
postgres_cursor.execute("INSERT INTO users (email, name) VALUES (%s, %s)", ("alice@example.com", "Duplicate Alice"))  # Should fail
```

#### **b) Transaction Atomicity**
- **Begins a transaction using `BEGIN;`**.
- **Inserts a record, then forces an error before commit**.
- **Ensures rollback occurs and no records are committed**.

```python
postgres_cursor.execute("BEGIN;")
postgres_cursor.execute("INSERT INTO orders (customer, amount) VALUES (%s, %s)", ("Bob", 50.00))
raise Exception("Simulating failure before commit.")  # Simulate error
postgres_cursor.execute("ROLLBACK;")  # Ensure atomicity
```

#### **c) Foreign Key Constraints**
- **Creates a `customers` table** as a parent.
- **Creates an `orders` table** with a foreign key constraint.
- **Attempts to insert an order for a non-existent customer** (should fail).

```python
postgres_cursor.execute("CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount DECIMAL(10,2), FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE)")
postgres_cursor.execute("INSERT INTO orders (customer_id, amount) VALUES (%s, %s)", (999, 25.00))  # Invalid FK
```

---

## **Key Takeaways**

### **Testcontainers**
- Provides a **lightweight, disposable PostgreSQL database** for testing.
- **No external dependencies** required.

### **PostgreSQL Constraints**
- Uses **unique constraints** to enforce data integrity.
- **Transactions ensure all-or-nothing execution**.
- **Foreign keys maintain referential integrity**.

### **Assertions**
- **Prevents duplicate records**.
- **Ensures valid data retrieval**.
- **Prevents inserting orphaned records**.

---

## **Troubleshooting**
### **Common Issues**
1. **Docker Not Running**  
   - Ensure Docker is installed and running:  
     ```bash
     docker ps
     ```

2. **ModuleNotFoundError: No module named 'psycopg2'**  
   - Install missing dependencies:  
     ```bash
     pip install psycopg2-binary
     ```

3. **PostgreSQL Testcontainer Failing to Start**  
   - Try allocating more memory to Docker.

---

## **Final Thoughts**
This test ensures **PostgreSQL correctly enforces data integrity** using **unique constraints, transactions, and foreign keys**.

---

🔥 **Happy Testing!** 🚀  

---

