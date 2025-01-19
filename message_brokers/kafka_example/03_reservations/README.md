# Example 03: Reservations

This example demonstrates how to handle reservations using Kafka as the message broker, focusing on the asynchronous processing of reservation requests. The example covers:

- Sending a message to create a reservation.
- Handling reservation confirmation.
- Error handling for reservation failures.

## Features

### Reservation Handling

- Send a message to the Kafka topic to create a new reservation.
- Confirm successful reservations through a response message.

### Error Handling

- Handle errors during the reservation process.
- Send appropriate error messages back to the client.

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For Kafka:
```bash
pip install kafka-python
```

or
```bash
pip3 install kafka-python
```

### 2. Run the Test

Execute the test file using pytest:

For Kafka:
```bash
python -m pytest 03_reservations.py -v -s
```

or
```bash
python3 -m pytest 03_reservations.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/dcbc43b8-38ed-4dcb-b837-6a5ce48e0a72)
