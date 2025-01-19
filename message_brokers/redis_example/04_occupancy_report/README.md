# Example 04: Occupancy Report

This example demonstrates how to generate occupancy reports using Redis as the data store. It focuses on simulating occupancy reports based on room booking and cancellation events. The example covers:

- Generating an occupancy report based on current reservations.
- Updating the report when reservations are added or removed.
- Handling edge cases such as overbooking.

## Features

### Occupancy Reporting

- Generate a report that summarizes current occupancy status.
- Update the report dynamically as reservations are made or cancelled.

### Error Handling

- Handle errors during report generation.
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
python -m pytest 04_occupancy_report.py -v -s
```

or
```bash
python3 -m pytest 04_occupancy_report.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/fa645c95-6cc0-44e7-8aba-4b5bfb01c3f8)

