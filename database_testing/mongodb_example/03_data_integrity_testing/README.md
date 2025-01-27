# Example 3: Data Integrity Testing (MongoDB)

This example demonstrates how to use **Testcontainers** to test **data integrity** in **MongoDB**. It ensures that:
- **Duplicate records are prevented** using **unique indexes**.
- **Data retrieval is consistent** after insertions.
- **Required fields are enforced** to prevent incomplete data storage.

---

## **Overview**

The test simulates a **real-world data validation scenario** by enforcing **data integrity** at the database level. It performs the following operations:

1. **Unique Constraint Testing**: Ensures duplicate email insertions are rejected.
2. **Insert & Retrieve Integrity**: Validates that records can be retrieved accurately.
3. **Missing Required Fields**: Tests if inserting a document without an `email` field is correctly handled.

Each operation is validated using **assertions** to ensure expected results.

---

## **Features**

### **MongoDB Container**
- Uses the `MongoDbContainer` class from **Testcontainers** to create a **temporary, isolated MongoDB database**.
- Automatically **starts and stops the container** before and after tests.

### **Data Integrity Checks**
- **Unique Indexing**: Ensures that the `email` field is unique.
- **Field Presence Validation**: Prevents inserting documents missing required fields.

### **Assertions**
- **Ensures data integrity** is properly enforced in MongoDB.
- **Prevents duplicate records** and validates correct storage & retrieval.

---

## **How to Run the Test**

### **1. Install Dependencies**
Ensure you have all required dependencies installed:

```bash
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
```

### **2. Run the Test**
Execute the test using `pytest`:

```bash
python -m pytest 03_data_integrity_testing.py -v -s
```

or

```bash
python3 -m pytest 03_data_integrity_testing.py -v -s
```

---

## **Expected Output**
When you run the test, you should see output similar to this:

![image](https://github.com/user-attachments/assets/c4975b78-b7e1-48ee-9221-8fec6baab60c)


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
The `mongodb_test_db` fixture initializes a **test database and collection**:

```python
db = mongodb_client.get_database("test_db")
collection = db.get_collection("data_integrity_test")
```

- The **test_db** database is created automatically.
- The **data_integrity_test** collection is used for validation.

### **3. Data Integrity Tests**
#### **a) Unique Constraint Testing**
- **Creates a unique index on the `email` field**.
- **Attempts duplicate inserts** and ensures failure.

```python
collection.create_index([("email", pymongo.ASCENDING)], unique=True)
collection.insert_one({"email": "alice@example.com", "name": "Alice"})
collection.insert_one({"email": "alice@example.com", "name": "Duplicate Alice"})  # Should fail
```

#### **b) Insert & Retrieve Integrity**
- Inserts a record and **retrieves it to verify correctness**.

```python
record = {"email": "bob@example.com", "name": "Bob"}
collection.insert_one(record)
retrieved_record = collection.find_one({"email": "bob@example.com"})
assert retrieved_record["name"] == "Bob"
```

#### **c) Missing Required Fields**
- Attempts to insert a document **without an `email` field** and expects rejection.

```python
collection.insert_one({"name": "Charlie"})  # Missing 'email'
```

---

## **Key Takeaways**

### **Testcontainers**
- Provides a **lightweight, disposable MongoDB database** for testing.
- **No external dependencies** required.

### **MongoDB Data Integrity**
- Uses **unique indexes** instead of transactions.
- Ensures **data correctness without application-level constraints**.

### **Assertions**
- **Prevents duplicate records**.
- **Ensures valid data retrieval**.
- **Prevents inserting incomplete records**.

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
This test ensures **MongoDB correctly enforces data integrity** using **indexes and constraints**.  
It is a **real-world alternative to transactions** and is widely applicable.

---

## **Next Steps**
You can extend this test by:
- Adding **more field constraints**.
- Testing **bulk inserts with unique constraints**.
- Simulating **database failures and recovery**.

---

🔥 **Happy Testing!** 🚀  
```

