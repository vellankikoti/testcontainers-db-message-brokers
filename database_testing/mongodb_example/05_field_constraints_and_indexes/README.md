# Example 5: Field Constraints & Index Testing (MongoDB)

This example demonstrates how to use **Testcontainers** to test **field constraints and indexing** in **MongoDB**. It ensures that:
- **Unique constraints** prevent duplicate entries.
- **Data type validation** ensures correct field values.
- **Indexes improve query performance**.

---

## **Overview**

The test simulates a **real-world data validation scenario** by enforcing **field-level constraints** and **indexing strategies** at the database level. It performs the following operations:

1. **Unique Index Enforcement**: Ensures that the `email` field does not allow duplicates.
2. **Data Type Constraints**: Ensures that `age` must be stored as an integer.
3. **Index Performance Optimization**: Ensures queries on indexed fields execute efficiently.

Each operation is validated using **assertions** to ensure expected results.

---

## **Features**

### **MongoDB Container**
- Uses **Testcontainers** to create a **temporary, isolated MongoDB database**.
- Automatically **starts and stops the container** before and after tests.

### **Field Constraints & Indexing**
- **Unique Indexing**: Prevents duplicate `email` values.
- **Data Type Validation**: Ensures `age` field stores only integers.
- **Index Performance Check**: Ensures indexed queries execute correctly.

### **Assertions**
- **Prevents invalid data insertion**.
- **Ensures indexing improves query performance**.

---

## **How to Run the Test**

### **1. Install Dependencies**
Ensure you have all required dependencies installed:

```bash
pip install -r requirements.txt
```

or

```bash
pip3 install -r requirements.txt
```

### **2. Run the Test**
Execute the test using `pytest`:

```bash
python3 -m pytest 05_field_constraints_and_indexes.py -v -s
```

---

## **Expected Output**
When you run the test, you should see output similar to this:

```bash
✅ Unique Index Constraint: Inserted first record successfully.
✅ Unique Index Constraint Passed: Duplicate Prevented.
✅ Data Type Constraint: Inserted valid age.
✅ Data Type Constraint Passed: Rejected incorrect age type.
✅ Index Performance Test Passed: Indexed query executed successfully.
```

If the test fails, possible errors might be:
- **Unique Index Failed** (Duplicate was allowed).
- **Data Type Constraint Failed** (Inserted incorrect data type).
- **Index Performance Test Failed** (Query did not return expected results).

---

## **Code Walkthrough**

### **1. MongoDB Container Setup**
The test uses **Testcontainers** to start a MongoDB instance inside a Docker container:

```python
with MongoDbContainer("mongo:latest") as mongo:
    yield mongo.get_connection_url()
```

- The container runs **MongoDB latest version**.
- The `get_connection_url()` method provides the **MongoDB connection string**.

### **2. Database Collection**
The `test_collection` fixture initializes a **test database and collection**:

```python
db = mongodb_client.get_database("test_db")
collection = db.get_collection("field_constraints_test")
```

- The **test_db** database is created automatically.
- The **field_constraints_test** collection is used for validation.

### **3. Field Constraints & Index Testing**
#### **a) Unique Index Enforcement**
- **Creates a unique index on the `email` field**.
- **Attempts duplicate inserts** and ensures failure.

```python
test_collection.create_index([("email", pymongo.ASCENDING)], unique=True)
test_collection.insert_one({"email": "alice@example.com", "name": "Alice"})
test_collection.insert_one({"email": "alice@example.com", "name": "Duplicate Alice"})  # Should fail
```

#### **b) Data Type Constraint (Age Must Be Integer)**
- Attempts to insert incorrect data types and expects rejection.

```python
test_collection.insert_one({"name": "Bob", "age": 30})  # Valid
test_collection.insert_one({"name": "Charlie", "age": "Thirty"})  # Should fail
```

#### **c) Index Performance Optimization**
- **Creates an index on `age`** to improve query performance.
- **Executes a query using the index** and ensures faster response.

```python
test_collection.create_index([("age", pymongo.ASCENDING)])
query_result = test_collection.find({"age": {"$gt": 25}})
```

---

## **Key Takeaways**

### **Testcontainers**
- Provides a **lightweight, disposable MongoDB database** for testing.
- **No external dependencies** required.

### **MongoDB Indexing & Constraints**
- Uses **unique indexes** to enforce data integrity.
- **Indexes improve query performance and efficiency**.
- Prevents **incorrect data types from being stored**.

### **Assertions**
- **Prevents duplicate records**.
- **Ensures valid data retrieval**.
- **Prevents inserting incorrect field types**.

---

## **Troubleshooting**
### **Common Issues**
1. **Docker Not Running**  
   - Ensure Docker is installed and running:  
     ```bash
     docker ps
     ```

2. **ModuleNotFoundError: No module named 'pymongo'**  
   - Install missing dependencies:  
     ```bash
     pip install pymongo
     ```

3. **MongoDB Testcontainer Failing to Start**  
   - Try allocating more memory to Docker.

---

## **Final Thoughts**
This test ensures **MongoDB correctly enforces field constraints & indexing** to **prevent invalid data storage and optimize performance**.

---

🔥 **Happy Testing!** 🚀  
```

---
