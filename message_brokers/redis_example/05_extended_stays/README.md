# Example 05: Extended Stays

This example demonstrates how to manage extended stays for guests using Redis as the data store. It focuses on handling requests for extending reservations and updating the corresponding records. The example covers:

- Requesting an extension for an existing reservation.
- Updating the reservation details in the database.
- Handling conflicts with other reservations.

## Features

### Extended Stay Management

- Allow guests to request an extension of their stay.
- Update the reservation details in Redis to reflect the new dates.
- Check for conflicts with existing reservations before confirming the extension.

### Error Handling

- Handle errors during the extension process.
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
python -m pytest 05_extended_stays.py -v -s
```

or
```bash
python3 -m pytest 05_extended_stays.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/2a67e68c-a64a-4866-a3a5-9a22a39756c4)

