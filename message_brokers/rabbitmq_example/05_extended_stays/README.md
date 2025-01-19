# Example 05: Extended Stays

This example demonstrates how to manage extended stays using a message broker, focusing on processing requests for long-term reservations. The example covers:

- Sending messages to create extended stay reservations.
- Handling confirmation and modification requests.
- Error handling for extended stay processing failures.

---

## Features

### Extended Stay Reservations

- Send a message to the message broker to create a new extended stay reservation.
- Confirm successful reservation creation through response messages.

### Modification Handling

- Handle requests to modify existing extended stay reservations.
- Send appropriate confirmation messages for modifications.

### Error Handling

- Handle errors during the extended stay reservation process.
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

```bash
python -m pytest 05_extended_stays.py -v -s
```
or
```bash
python3 -m pytest 05_extended_stays.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/2054b14a-0381-45f7-b039-0ee14cb79848)
