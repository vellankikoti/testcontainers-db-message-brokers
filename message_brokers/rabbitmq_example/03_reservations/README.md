# Example 03: Reservations

This example demonstrates how to handle reservations using a message broker, focusing on sending reservation requests and confirmations asynchronously. The example covers:

- Sending messages to create a reservation.
- Handling reservation confirmations.
- Error handling for reservation failures.

---

## Features

### Reservation Creation

- Send a message to the message broker to create a new reservation.
- Confirm successful reservation creation through a response message.

### Error Handling

- Handle errors during the reservation process.
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
python -m pytest 03_reservations.py -v -s
```
or
```bash
python3 -m pytest 03_reservations.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/49137c32-bdd7-47ce-af05-92b94abf6538)

