# Example 5: Field Constraints & Index Testing (MySQL)

This example demonstrates how to use **Testcontainers** to test **field constraints and indexing** in **MySQL**. It ensures that:
- **NOT NULL constraints** prevent missing values.
- **CHECK constraints** enforce valid data ranges.
- **Indexes improve query performance**.

---

## **Overview**

The test simulates **real-world data validation scenarios** using MySQL. It performs the following operations:

1. **NOT NULL Constraint Enforcement**: Ensures that `NULL` values cannot be inserted in required fields.
2. **CHECK Constraint Validation**: Ensures that **invalid values are rejected** (e.g., age cannot be below 18).
3. **Index Performance Optimization**: Ensures that indexed queries execute efficiently.

Each operation is validated using **assertions** to ensure expected results.

---

## **Features**

### **MySQL Container**
- Uses **Testcontainers** to create a **temporary, isolated MySQL database**.
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
pip install pytest testcontainers mysql-connector-python
```

#### **Using `pip3`**
```bash
pip3 install pytest testcontainers mysql-connector-python
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

![image](https://github.com/user-attachments/assets/eb4e563f-e89a-4ac0-8097-f9926fde581d)

---

If the test fails, possible errors might be:
- **NOT NULL Constraint Failed** (NULL values were allowed).
- **CHECK Constraint Failed** (Invalid values were inserted).
- **Index Performance Test Failed** (Query did not return expected results).

---

## **Code Walkthrough**

### **1. MySQL Container Setup**
The test uses **Testcontainers** to start a MySQL instance inside a Docker container:

```python
with MySqlContainer("mysql:latest") as mysql:
    yield mysql.get_connection_url()
```

- The container runs **MySQL latest version**.
- The `get_connection_url()` method provides the **MySQL connection string**.

### **2. Database Connection**
The `mysql_cursor` fixture initializes a **test database connection**:

```python
connection = mysql.connector.connect(
    host=mysql_container.get_container_host_ip(),
    port=mysql_container.get_exposed_port(3306),
    user="test",
    password="test",
    database="test"
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
mysql_cursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, price DECIMAL(10,2) NOT NULL)")
mysql_cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (None, None))  # Should fail
```

#### **b) CHECK Constraint Validation**
- **Creates a table with a `CHECK` constraint on `age`**.
- **Attempts to insert an invalid age (`15`), which should be rejected**.

```python
mysql_cursor.execute("CREATE TABLE employees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, age INT CHECK (age >= 18))")
mysql_cursor.execute("INSERT INTO employees (name, age) VALUES (%s, %s)", ("Bob", 15))  # Should fail
```

#### **c) Index Performance Optimization**
- **Creates an index on the `salary` column** to improve query performance.
- **Executes a query using the indexed field** and ensures correct results.

```python
mysql_cursor.execute("CREATE TABLE employees (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, salary DECIMAL(10,2) NOT NULL, INDEX (salary))")
mysql_cursor.execute("SELECT COUNT(*) FROM employees WHERE salary > 55000")
```

---

## **Key Takeaways**

### **Testcontainers**
- Provides a **lightweight, disposable MySQL database** for testing.
- **No external dependencies** required.

### **MySQL Constraints**
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

2. **ModuleNotFoundError: No module named 'mysql.connector'**  
   - Install missing dependencies:  
     ```bash
     pip install mysql-connector-python
     ```

3. **MySQL Testcontainer Failing to Start**  
   - Try allocating more memory to Docker.

---

## **Final Thoughts**
This test ensures **MySQL correctly enforces field constraints & indexing** to **prevent invalid data storage and optimize performance**.

---

🔥 **Happy Testing!** 🚀  

---
