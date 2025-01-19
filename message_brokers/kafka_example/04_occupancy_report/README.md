# Example 04: Occupancy Report

This example demonstrates how to generate occupancy reports using Kafka as the message broker, focusing on the asynchronous processing of report requests. The example covers:

- Sending a message to request an occupancy report.
- Handling report generation confirmation.
- Error handling for report generation failures.

## Features

### Occupancy Reporting

- Send a message to the Kafka topic to request an occupancy report.
- Confirm successful report generation through a response message.

### Error Handling

- Handle errors during the report generation process.
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
python -m pytest 04_occupancy_report.py -v -s
```

or
```bash
python3 -m pytest 04_occupancy_report.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/ef15149c-0b3b-4709-992f-109d76f65ec5)

