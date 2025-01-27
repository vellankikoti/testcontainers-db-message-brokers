# Example 5: Kafka Field Constraints & Data Integrity Testing

This example demonstrates how to use **Testcontainers** to test **field constraints and data integrity** in **Kafka**. It ensures that:

- **Message schema enforcement** prevents incorrect data formats.
- **Duplicate message prevention** maintains data accuracy.
- **Message ordering** is preserved across production and consumption.

---

## **Overview**

This test simulates a **real-world Kafka data validation scenario** by enforcing **schema validation, duplicate prevention, and ordered message processing**. It performs the following operations:

1. **Message Schema Enforcement**: Ensures messages adhere to a predefined schema before being sent.
2. **Duplicate Message Prevention**: Ensures no duplicate messages are produced or consumed.
3. **Message Ordering Validation**: Ensures Kafka preserves the order of messages.
4. **Invalid Message Handling**: Ensures incorrect messages are rejected.

Each operation is validated using **assertions** to ensure the expected results.

---

## **Features**

### **Kafka Container**
- Uses **Testcontainers** to create a **temporary, isolated Kafka broker**.
- Automatically **starts and stops the container** before and after tests.

### **Field Constraints & Data Integrity**
- **Schema Enforcement**: Ensures messages follow a structured format.
- **Duplicate Prevention**: Ensures no duplicate messages are processed.
- **Ordering Validation**: Ensures messages are consumed in the order they were produced.

### **Assertions**
- **Prevents invalid message formats** from being published.
- **Ensures messages follow schema constraints**.
- **Validates message ordering and uniqueness**.

---

## **How to Run the Test**

### **1. Install Dependencies**
Ensure you have all required dependencies installed:

```bash
pip install pytest testcontainers kafka-python
```

or

```bash
pip3 install pytest testcontainers kafka-python
```

### **2. Run the Test**
Execute the test using `pytest`:

```bash
python3 -m pytest 05_kafka_field_constraints.py -v -s
```

or

```bash
python -m pytest 05_kafka_field_constraints.py -v -s
```

---

## **Expected Output**
When you run the test, you should see output similar to this:

```plaintext
Producing valid messages to Kafka...
✅ Valid messages successfully produced!

Producing invalid messages to Kafka...
❌ Invalid message rejected as expected!

Consuming messages from Kafka...

Validating message order and uniqueness...
✅ Kafka data integrity validation PASSED! 🎉
```

If the test fails, possible errors might be:
- **Schema Enforcement Failed** (Invalid message was published).
- **Duplicate Message Check Failed** (Duplicate message detected).
- **Message Order Check Failed** (Messages were consumed out of order).

---

## **Code Walkthrough**

### **1. Kafka Container Setup**
The test uses **Testcontainers** to start a Kafka broker inside a Docker container:

```python
with KafkaContainer("confluentinc/cp-kafka:latest") as kafka:
    yield kafka.get_bootstrap_server()
```

- The container runs **Kafka latest version**.
- The `get_bootstrap_server()` method provides the **Kafka connection string**.

### **2. Message Schema Validation**
The test enforces a schema for Kafka messages:

```python
def validate_message_schema(message):
    schema = {"id": int, "name": str, "email": str}
    return all(key in message and isinstance(message[key], schema[key]) for key in schema)
```

- Messages must contain `id` (integer), `name` (string), and `email` (string).
- If a message does not match the schema, it **should not be published**.

### **3. Producing Messages**
Valid messages are sent to Kafka:

```python
messages_sent = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

for message in messages_sent:
    producer.send("field_constraints_topic", json.dumps(message).encode("utf-8"))
```

- Messages are **JSON-encoded** before publishing.

### **4. Consuming Messages & Validating Order**
Messages are consumed and validated:

```python
consumer = KafkaConsumer(
    "field_constraints_topic",
    bootstrap_servers=kafka_bootstrap_server,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=5000
)

messages_received = [json.loads(msg.value) for msg in consumer]

assert messages_received == messages_sent, "Message order was not preserved!"
```

- Ensures **messages are received in the correct order**.

### **5. Preventing Duplicate Messages**
The test ensures **no duplicate messages** were published:

```python
assert len(messages_received) == len(set(json.dumps(m) for m in messages_received)), "Duplicate messages detected!"
```

- Converts messages to JSON strings and uses a **set** to check for duplicates.

### **6. Rejecting Invalid Messages**
The test attempts to send an **invalid message**:

```python
invalid_message = {"id": "wrong_type", "name": "Charlie"}
assert not validate_message_schema(invalid_message), "Invalid message should be rejected!"
```

- Ensures the **invalid message is not accepted**.

---

## **Key Takeaways**

### **Testcontainers**
- Provides a **lightweight, disposable Kafka broker** for testing.
- **No external dependencies** required.

### **Kafka Data Constraints**
- **Schema validation ensures structured data**.
- **Prevents duplicate messages**.
- **Validates ordering for reliable processing**.

### **Assertions**
- **Prevents invalid data from being published**.
- **Ensures message schema compliance**.
- **Verifies correct message ordering and uniqueness**.

---

## **Troubleshooting**
### **Common Issues**
1. **Docker Not Running**  
   - Ensure Docker is installed and running:  
     ```bash
     docker ps
     ```

2. **ModuleNotFoundError: No module named 'kafka'**  
   - Install missing dependencies:  
     ```bash
     pip install kafka-python
     ```

3. **Kafka Testcontainer Failing to Start**  
   - Check available memory and **restart Docker** if needed.

---

## **Final Thoughts**
This test ensures **Kafka correctly enforces schema constraints, prevents duplicates, and maintains message order**. This is **critical for real-world event-driven architectures**.

---

🔥 **Happy Testing!** 🚀
