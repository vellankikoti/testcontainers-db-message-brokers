# **Example 5: Field Constraints & Index Testing (Redis)**  

This example demonstrates how to use **Testcontainers** to test **field constraints and indexing** in **Redis**. It ensures that:  
- **Key constraints** enforce data integrity.  
- **Data type validation** prevents incorrect value storage.  
- **TTL (Time-To-Live) constraints** ensure automatic data expiration.  

---

## **Overview**  

The test simulates a **real-world Redis data validation scenario** by enforcing **key constraints, expiration rules, and data integrity mechanisms**. It performs the following operations:  

1. **Unique Key Enforcement**: Ensures that Redis keys are unique and do not get overwritten accidentally.  
2. **Data Type Constraints**: Ensures that values are stored as expected (e.g., strings, integers, lists).  
3. **TTL Constraints**: Ensures that Redis keys expire as expected when a time-to-live (TTL) is set.  

Each operation is validated using **assertions** to ensure expected results.  

---

## **Features**  

### **Redis Container**  
- Uses **Testcontainers** to create a **temporary, isolated Redis instance**.  
- Automatically **starts and stops the container** before and after tests.  

### **Field Constraints & Indexing**  
- **Unique Key Constraints**: Ensures Redis does not overwrite existing keys when `SETNX` is used.  
- **Data Type Enforcement**: Ensures correct types are stored in Redis (e.g., integers in `INCR`, lists in `LPUSH`).  
- **TTL Constraints**: Ensures keys expire automatically after the specified time.  

### **Assertions**  
- **Prevents accidental key overwrites**.  
- **Ensures data type integrity**.  
- **Validates Redis key expiration (TTL) works correctly**.  

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

![image](https://github.com/user-attachments/assets/00314357-653b-434e-a009-b7497fb5ce45)

---

If the test fails, possible errors might be:  
- **Unique key constraint failed** (Duplicate key was allowed).  
- **Data type validation failed** (Inserted incorrect data type).  
- **TTL expiration test failed** (Key did not expire within the expected time).  

---

## **Code Walkthrough**  

### **1. Redis Container Setup**  

The test uses **Testcontainers** to start a Redis instance inside a Docker container:  

```python
with RedisContainer("redis:latest") as redis:
    yield redis.get_connection_url()
```  

- The container runs **Redis latest version**.  
- The `get_connection_url()` method provides the **Redis connection string**.  

---

### **2. Database Connection**  

The `redis_client` fixture initializes a **test Redis connection**:  

```python
redis_client = redis.Redis(host=redis_container.get_container_host_ip(),
                           port=redis_container.get_exposed_port(6379),
                           decode_responses=True)
```  

- The **Redis client** connects to the running **Testcontainers Redis instance**.  
- **decode_responses=True** ensures stored values are returned as strings.  

---

### **3. Field Constraints & Index Testing**  

#### **a) Unique Key Enforcement**  

- **Uses `SETNX` (Set if Not Exists)** to ensure duplicate keys are not stored.  
- **Attempts duplicate key insertions** and ensures failure.  

```python
result1 = redis_client.setnx("unique_key", "First Value")  # Should succeed
result2 = redis_client.setnx("unique_key", "Duplicate Value")  # Should fail

assert result1 == 1, "⚠️ Unique key insertion failed!"
assert result2 == 0, "⚠️ Duplicate key was allowed!"
```  

✅ Ensures **duplicate keys cannot be overwritten using `SETNX`**.  

---

#### **b) Data Type Constraints**  

- **Ensures integers are used in `INCR` operations**.  
- **Ensures lists are stored correctly using `LPUSH`**.  

```python
redis_client.set("int_key", 5)  # Store an integer
redis_client.incr("int_key")  # Increment integer value
value = redis_client.get("int_key")

assert value == "6", "⚠️ Data type integrity failed for integers!"

redis_client.lpush("list_key", "item1", "item2")  # Store a list
list_values = redis_client.lrange("list_key", 0, -1)

assert list_values == ["item2", "item1"], "⚠️ List storage integrity failed!"
```  

✅ Ensures **Redis enforces correct data types**.  

---

#### **c) TTL Constraints (Key Expiration)**  

- **Sets a key with an expiration time of 3 seconds**.  
- **Waits for 4 seconds** and ensures the key is deleted.  

```python
redis_client.setex("ttl_key", 3, "Temporary Data")

time.sleep(4)  # Allow key to expire

expired_value = redis_client.get("ttl_key")
assert expired_value is None, "⚠️ Expired key still exists!"
```  

✅ Ensures **data expires properly and does not persist beyond its TTL**.  

---

## **Key Takeaways**  

### **Testcontainers for Redis**  
- Provides a **lightweight, disposable Redis instance** for testing.  
- **No external dependencies** required.  

### **Redis Key Constraints & Expiration**  
- Uses **SETNX** to **prevent accidental overwrites**.  
- **Ensures correct data types** for different storage operations.  
- **Validates TTL expiration for temporary data**.  

### **Assertions**  
- **Prevents duplicate key overwrites**.  
- **Ensures valid data retrieval**.  
- **Checks for correct key expiration behavior**.  

---

## **Troubleshooting**  

### **Common Issues**  

1. **Docker Not Running**  
   - Ensure Docker is installed and running:  
     ```bash
     docker ps
     ```  

2. **ModuleNotFoundError: No module named 'redis'**  
   - Install missing dependencies:  
     ```bash
     pip install redis
     ```  

3. **Redis Testcontainer Failing to Start**  
   - Try allocating more memory to Docker.  

---

## **Final Thoughts**  

This test ensures **Redis correctly enforces field constraints & TTL expiration** to **prevent invalid data storage and optimize performance**.  

---

## **Next Steps**  

You can extend this test by:  
- **Testing set expiration policies in bulk operations**.  
- **Validating different Redis data structures (sorted sets, hashes, streams)**.  
- **Simulating Redis failures and recovery scenarios**.  

---

🔥 **Happy Testing!** 🚀  
