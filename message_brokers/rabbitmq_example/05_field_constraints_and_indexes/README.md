# **Example 5: RabbitMQ Field Constraints and Index Testing**

This example demonstrates how to use **Testcontainers** to test **message constraints in RabbitMQ**. It covers the following:

- Setting up a RabbitMQ container.
- Enforcing message schema validation.
- Limiting message size to prevent oversized messages.
- Ensuring unique message identifiers (index constraints).

---

## **Overview**

The test ensures that RabbitMQ:
1. **Validates message structure** before processing.
2. **Rejects oversized messages** exceeding a defined size.
3. **Detects duplicate message IDs** to prevent conflicts.

This helps maintain **data integrity** in real-world RabbitMQ applications.

---

## **Features**

### **RabbitMQ Container**
- Uses the `RabbitMqContainer` class from the `testcontainers` library to start a RabbitMQ broker.
- Automatically handles container lifecycle (start and stop).
- Provides an isolated testing environment.

### **Field Constraints Validation**
- **Ensures messages have the required fields** (`id`, `name`, `timestamp`, `priority`).
- **Rejects messages that exceed 1 KB**.
- **Prevents duplicate IDs from being processed**.

### **Assertions**
- Ensures **message schema compliance**.
- Validates **message size restrictions**.
- Checks **unique message indexing**.

---

## **How to Run the Test**

### **1. Install Dependencies**
Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pika
```

or

```bash
pip3 install pytest testcontainers pika
```

### **2. Run the Test**
Execute the test file using `pytest`:

```bash
python -m pytest 05_field_constraints_and_indexes.py -v -s
```

or

```bash
python3 -m pytest 05_field_constraints_and_indexes.py -v -s
```

---

## **Expected Output**

When you run the test, you should see output similar to:



---

## **Code Walkthrough**

### **1. RabbitMQ Container Setup**
The test uses the `RabbitMqContainer` class to start a RabbitMQ broker in a Docker container:

```python
with RabbitMqContainer("rabbitmq:3.9-management") as rabbitmq:
    yield rabbitmq
```

- The container runs **RabbitMQ 3.9 with management tools**.
- It provides the **AMQP connection URL**.

---

### **2. Message Schema Validation**
The test ensures that each message contains the required fields:

```python
def validate_message_schema(message):
    required_fields = {"id", "name", "timestamp", "priority"}
    return required_fields.issubset(message.keys())
```

- If a required field is missing, the test **fails**.

---

### **3. Message Size Limit**
The test enforces a **1 KB limit** for each message:

```python
MAX_MESSAGE_SIZE = 1024  # 1 KB limit

def validate_message_size(message):
    return len(json.dumps(message).encode("utf-8")) <= MAX_MESSAGE_SIZE
```

- If a message exceeds **1024 bytes**, it is **blocked**.

---

### **4. Preventing Duplicate IDs**
RabbitMQ does **not** enforce unique message IDs by default. This test ensures each message has a **unique ID** before processing:

```python
seen_ids = set()

for message in messages:
    assert message["id"] not in seen_ids, f"⚠️ Duplicate ID detected: {message['id']}"
    seen_ids.add(message["id"])
```

- If a **duplicate ID is detected**, the test **fails**.

---

## **Key Takeaways**

### **Testcontainers for RabbitMQ**
- Provides **an isolated, disposable RabbitMQ instance**.
- Ensures **test reproducibility**.

### **Message Constraints Validation**
- **Schema validation ensures messages follow a strict format**.
- **Message size constraints prevent system overloads**.
- **Unique indexing prevents duplicate processing**.

### **Assertions**
- **Ensures correct message formatting**.
- **Prevents oversized messages**.
- **Checks for duplicate message IDs**.

---

## **Troubleshooting**

### **Common Issues**

1. **Docker Not Running**  
   - Ensure Docker is installed and running:
     ```bash
     docker ps
     ```

2. **ModuleNotFoundError: No module named 'pika'**  
   - Install the missing dependency:
     ```bash
     pip install pika
     ```

3. **RabbitMQ Testcontainer Failing to Start**  
   - Try allocating more memory to Docker.

---

## **Next Steps**

You can extend this test by:
- **Adding more complex schema validation (JSON schema, Avro, Protobuf).**
- **Simulating message failures and retries.**
- **Testing performance with high-volume message processing.**

---

🔥 **Happy Testing with RabbitMQ and Testcontainers!** 🚀

---
