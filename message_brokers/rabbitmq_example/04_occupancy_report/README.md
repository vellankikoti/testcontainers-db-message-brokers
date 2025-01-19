# Example 04: Occupancy Report

This example demonstrates how to generate an occupancy report using a message broker, focusing on collecting and processing occupancy data asynchronously. The example covers:

- Sending messages to collect occupancy data.
- Handling responses to generate reports.
- Error handling for report generation failures.

---

## Features

### Occupancy Data Collection

- Send a message to the message broker to collect occupancy data from various sources.
- Confirm successful data collection through response messages.

### Report Generation

- Generate occupancy reports based on the collected data.
- Provide insights into room usage and availability.

### Error Handling

- Handle errors during the data collection and report generation process.
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
python -m pytest 04_occupancy_report.py -v -s
```
or
```bash
python3 -m pytest 04_occupancy_report.py -v -s
```

---

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/0dd7d9a4-eeb7-495d-9547-18b44c428005)

