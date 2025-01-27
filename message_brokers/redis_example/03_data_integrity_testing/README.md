# **Example 3: Data Integrity Testing (Redis)**  

This example demonstrates how to use **Testcontainers** to test **data integrity** in **Redis**. It ensures that:  
- **Duplicate keys are prevented** using **set operations**.  
- **Data retrieval is consistent** after insertions.  
- **Expiration policies work correctly**, ensuring **data doesn't persist longer than expected**.  

---

## **Overview**  

The test simulates a **real-world data validation scenario** by enforcing **data integrity** at the Redis level. It performs the following operations:  

1. **Unique Key Testing**: Ensures that duplicate keys are not stored.  
2. **Insert & Retrieve Integrity**: Validates that data can be retrieved accurately.  
3. **Expiration Testing**: Ensures keys expire as expected when TTL (Time-To-Live) is set.  

Each operation is validated using **assertions** to ensure expected results.  

---

## **Features**  

### **Redis Container**  
- Uses the `RedisContainer` class from **Testcontainers** to create a **temporary, isolated Redis database**.  
- Automatically **starts and stops the container** before and after tests.  

### **Data Integrity Checks**  
- **Set Operations**: Ensures that duplicate records are avoided when using `SETNX`.  
- **Expiration Policies**: Ensures key expiry functionality works as expected.  
- **Data Retrieval**: Validates that stored values match expected results.  

### **Assertions**  
- **Ensures Redis enforces unique keys** where applicable.  
- **Validates expiration rules** for temporary data.  
- **Ensures consistent data retrieval** after inserts.  

---

## **How to Run the Test**  

### **1. Install Dependencies**  

Ensure you have all required dependencies installed:  

```bash
pip install pytest testcontainers redis
```  

or  

```bash
pip3 install pytest testcontainers redis
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

![image](https://github.com/user-attachments/assets/8ed5f83e-0824-4958-b7f6-91563873a0d7)

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

### **3. Data Integrity Tests**  

#### **a) Unique Key Testing (Avoiding Overwrites)**  

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

#### **b) Insert & Retrieve Integrity**  

- **Inserts a key-value pair and retrieves it** to validate correctness.  

```python
redis_client.set("data_key", "Redis Integrity Test")
retrieved_value = redis_client.get("data_key")

assert retrieved_value == "Redis Integrity Test", "⚠️ Data integrity mismatch!"
```  

✅ Ensures **stored values match the expected data**.  

---

#### **c) Expiration Testing (TTL Validation)**  

- **Sets a key with an expiration time of 2 seconds**.  
- **Waits for 3 seconds** and ensures the key is deleted.  

```python
redis_client.setex("temp_key", 2, "Temporary Data")

time.sleep(3)  # Allow key to expire

expired_value = redis_client.get("temp_key")
assert expired_value is None, "⚠️ Expired key still exists!"
```  

✅ Ensures **data expires properly and does not persist beyond its TTL**.  

---

## **Key Takeaways**  

### **Testcontainers for Redis**  
- Provides a **lightweight, disposable Redis database** for testing.  
- **No external dependencies** required.  

### **Redis Data Integrity**  
- Uses **SETNX** for **unique key constraints**.  
- Validates **correct data retrieval** after inserts.  
- Ensures **keys expire correctly** when TTL is set.  

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

This test ensures **Redis correctly enforces data integrity** using **key constraints and expiration policies**.  
It is a **real-world alternative to database-level constraints** and is widely applicable in caching and session management scenarios.  

---

## **Next Steps**  

You can extend this test by:  
- Adding **more data validation constraints**.  
- Testing **bulk operations with expiration rules**.  
- Simulating **Redis failures and recovery**.  

---

🔥 **Happy Testing!** 🚀  
