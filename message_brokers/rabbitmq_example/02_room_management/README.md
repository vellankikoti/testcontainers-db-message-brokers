# Example 02: Room Management

This example demonstrates how to manage room details using a message broker, focusing on updating room status and availability asynchronously. The example covers:

- Sending messages to update room details.
- Handling room status updates.
- Error handling for update failures.

---

## Features

### Room Status Management

- Send a message to the message broker to update the status of a room (e.g., available, occupied, maintenance).
- Confirm successful updates through response messages.

### Error Handling

- Handle errors during the room update process.
- Send appropriate error messages back to the client.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For RabbitMQ:
```bash
pip install pika
```
or
```bash
pip3 install pika
```

For Kafka:
```bash
pip install kafka-python
```
or
```bash
pip3 install kafka-python
```

For Redis:
```bash
pip install redis
```
or
```bash
pip3 install redis
```

---

### 2. Run the Test

Execute the test file using pytest:

For RabbitMQ:
```bash
python -m pytest 02_room_management.py -v -s
```
or
```bash
python3 -m pytest 02_room_management.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/153b48cb-4d32-44fb-a358-12716c59be1f)
