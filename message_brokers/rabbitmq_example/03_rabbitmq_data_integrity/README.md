# **Example 3: RabbitMQ Data Integrity Testing**

This example demonstrates how to use **Testcontainers** to test **RabbitMQ data integrity**. It covers the following:

- Setting up a RabbitMQ container.
- Publishing messages to a RabbitMQ queue.
- Validating message ordering and uniqueness.
- Ensuring message integrity upon consumption.

---

## **Overview**

The test ensures that RabbitMQ maintains **message integrity, ordering, and uniqueness** when messages are published and consumed. It performs the following operations:

1. **Publish Messages** – Send multiple messages to a RabbitMQ queue.
2. **Consume Messages** – Retrieve messages from the queue.
3. **Validate Data Integrity** – Ensure messages are received in order, with no duplicates.

---

## **Features**

### **RabbitMQ Container**

- Uses the `RabbitMQContainer` class from the `testcontainers` library to spin up a RabbitMQ instance in a Docker container.
- Automatically handles container lifecycle (start and stop).

### **Data Integrity Validation**

- Ensures **RabbitMQ maintains message order**.
- Verifies that **no duplicate messages** exist.
- Ensures **all messages are accurately retrieved**.

### **Assertions**

- Validates **message ordering, uniqueness, and completeness**.

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
python -m pytest 03_rabbitmq_data_integrity.py -v -s
```

or

```bash
python3 -m pytest 03_rabbitmq_data_integrity.py -v -s
```

---

## **Expected Output**

When you run the test, you should see output similar to the following:

```
=================================== test session starts ===================================
...
Produced: Message 1
Produced: Message 2
Produced: Message 3

Consumed: Message 1
Consumed: Message 2
Consumed: Message 3

✅ RabbitMQ Data Integrity Test Passed!
=================================== 1 passed in X seconds =================================
```

---

## **Code Walkthrough**

### **1. RabbitMQ Container Setup**

The test uses the `RabbitMQContainer` class to start a RabbitMQ broker in a Docker container:

```python
with RabbitMQContainer("rabbitmq:latest") as rabbitmq:
    yield rabbitmq.get_connection_url()
```

- The container runs the **latest version of RabbitMQ**.
- The `get_connection_url()` method provides the **AMQP connection string** for RabbitMQ clients.

---

### **2. Publishing Messages**

The test publishes multiple messages to a RabbitMQ queue:

```python
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
channel = connection.channel()
channel.queue_declare(queue="data_integrity_queue")

messages_sent = ["Message 1", "Message 2", "Message 3"]

for message in messages_sent:
    channel.basic_publish(exchange="", routing_key="data_integrity_queue", body=message)
    print(f"Produced: {message}")

connection.close()
```

- Declares a **queue named `data_integrity_queue`**.
- Sends three messages (`Message 1`, `Message 2`, `Message 3`) to the queue.

---

### **3. Consuming Messages**

After messages are published, the test retrieves them from RabbitMQ:

```python
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
channel = connection.channel()

messages_received = []

for method_frame, properties, body in channel.consume("data_integrity_queue", auto_ack=True):
    messages_received.append(body.decode())
    print(f"Consumed: {body.decode()}")

    if len(messages_received) == len(messages_sent):
        break  # Stop consuming once all messages are received

connection.close()
```

- Subscribes to **`data_integrity_queue`**.
- Collects all received messages.

---

### **4. Data Integrity Validation**

The test uses assertions to validate RabbitMQ's data integrity:

```python
assert messages_received == messages_sent, "Message order was not preserved!"
assert len(messages_received) == len(set(messages_received)), "Duplicate messages detected!"
assert set(messages_received) == set(messages_sent), "Some messages are missing!"
```

- Ensures **message order is preserved**.
- Ensures **no duplicate messages** exist.
- Ensures **all messages were successfully retrieved**.

---

## **Key Takeaways**

### **Testcontainers for RabbitMQ**

- Simplifies testing by providing **lightweight, disposable RabbitMQ containers**.
- Automatically manages the **container lifecycle**.

### **RabbitMQ Data Integrity**

- Demonstrates **RabbitMQ's ability to maintain message order and uniqueness**.
- Ensures **reliability of RabbitMQ messaging systems**.

### **Assertions**

- Validates **message ordering, uniqueness, and completeness**.

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
- **Testing high-volume messaging scenarios**.
- **Simulating message failures and retries**.
- **Validating performance under load**.

---

🔥 **Happy Testing with RabbitMQ and Testcontainers!** 🚀
