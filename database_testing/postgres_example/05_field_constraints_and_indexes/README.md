# Example 5: Field Constraints & Index Testing (PostgreSQL)

This example demonstrates how to use **Testcontainers** to test **field constraints and indexing** in **PostgreSQL**. It ensures that:
- **NOT NULL constraints** prevent missing values.
- **CHECK constraints** enforce valid data ranges.
- **Indexes improve query performance**.

---

## **Overview**

The test simulates **real-world data validation scenarios** using PostgreSQL. It performs the following operations:

1. **NOT NULL Constraint Enforcement**: Ensures that `NULL` values cannot be inserted in required fields.
2. **CHECK Constraint Validation**: Ensures that **invalid values are rejected** (e.g., age cannot be below 18).
3. **Index Performance Optimization**: Ensures that indexed queries execute efficiently.

Each operation is validated using **assertions** to ensure expected results.

---

## **Features**

### **PostgreSQL Container**
- Uses **Testcontainers** to create a **temporary, isolated PostgreSQL database**.
- Automatically **starts and stops the container** before and after tests.

### **Field Constraints & Indexing**
- **NOT NULL Constraints**: Ensures that mandatory fields cannot have NULL values.
- **CHECK Constraints**: Restricts values to valid ranges (e.g., age must be 18 or above).
- **Index Performance Check**: Ensures indexed queries execute efficiently.

### **Assertions**
- **Prevents NULL values** in required fields.
- **Ensures valid data retrieval** using constraints.
- **Verifies indexing improves query performance**.

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
python -m pytest 05_field_constraints_and_indexes.py -v -s
```

#### **Using Python 3/Linux/macOS**
```bash
python3 -m pytest 05_field_constraints_and_indexes.py -v -s
```

---

## **Expected Output**
When you run the test, you should see output similar to this:


---

If the test fails, possible errors might be:
- **NOT NULL Constraint Failed** (NULL values were allowed).
- **CHECK Constraint Failed** (Invalid values were inserted).
- **Index Performance Test Failed** (Query did not return expected results).

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

### **3. Field Constraints & Index Testing**
#### **a) NOT NULL Constraint Enforcement**
- **Creates a table with `NOT NULL` constraints on `name` and `price`**.
- **Attempts to insert a `NULL` value**, which should be rejected.

```python
postgres_cursor.execute("CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, price DECIMAL(10,2) NOT NULL)")
postgres_cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (None, None))  # Should fail
```

#### **b) CHECK Constraint Validation**
- **Creates a table with a `CHECK` constraint on `age`**.
- **Attempts to insert an invalid age (`15`), which should be rejected**.

```python
postgres_cursor.execute("CREATE TABLE employees (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT CHECK (age >= 18))")
postgres_cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", ("Bob", 15))  # Should fail
```

#### **c) Index Performance Optimization**
- **Creates an index on the `salary` column** to improve query performance.
- **Executes a query using the indexed field** and ensures correct results.

```python
postgres_cursor.execute("CREATE TABLE employees (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL, salary DECIMAL(10,2) NOT NULL, INDEX (salary))")
postgres_cursor.execute("SELECT COUNT(*) FROM employees WHERE salary > 55000")
```

---

## **Key Takeaways**

### **Testcontainers**
- Provides a **lightweight, disposable PostgreSQL database** for testing.
- **No external dependencies** required.

### **PostgreSQL Constraints**
- Uses **NOT NULL constraints** to enforce data integrity.
- **CHECK constraints ensure values remain within valid ranges**.
- **Indexes improve query efficiency**.

### **Assertions**
- **Prevents NULL values in required fields**.
- **Ensures valid data retrieval**.
- **Prevents inserting out-of-range values**.

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
This test ensures **PostgreSQL correctly enforces field constraints & indexing** to **prevent invalid data storage and optimize performance**.

---

🔥 **Happy Testing!** 🚀  

---
