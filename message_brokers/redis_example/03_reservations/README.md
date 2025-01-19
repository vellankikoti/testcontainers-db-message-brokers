# Example 03: Reservations

This example demonstrates how to handle room reservations using Redis as the data store. It focuses on the implementation of Kafka producers and consumers to manage room reservations, cancellations, and updates. The example covers:

- Creating a new reservation.
- Cancelling an existing reservation.
- Updating reservation details.

## Features

### Reservation Management

- Create a new reservation by sending a message to the Redis database.
- Cancel an existing reservation and update the status in the database.
- Retrieve reservation details for confirmation.

### Error Handling

- Handle errors during reservation operations.
- Provide appropriate error messages for failed operations.

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

For Redis:
```bash
pip install redis
```

or
```bash
pip3 install redis
```

### 2. Run the Test

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 03_reservations.py -v -s
```

or
```bash
python3 -m pytest 03_reservations.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/d8742454-cea0-4ba3-a6e3-ec24072febb2)

---

