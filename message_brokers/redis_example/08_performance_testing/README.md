# Example 08: Performance Testing

This example demonstrates how to conduct performance testing on the reservation system using Redis as the data store. It focuses on measuring the system's response times and throughput under various load conditions. The example covers:

- Setting up performance tests using a load testing tool.
- Measuring response times for different operations.
- Analyzing the results to identify bottlenecks.

## Features

### Performance Testing

- Use a load testing tool (e.g., Locust or JMeter) to simulate multiple users.
- Measure response times for operations such as reservations and cancellations.
- Analyze throughput and identify performance bottlenecks.

### Error Handling

- Handle errors during performance testing.
- Provide appropriate error messages for failed tests or unexpected results.

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
### Run the Script
```bash
python3 -m pytest -v 08_performance_testing.py
```
 or
 ```bash
python -m pytest -v 08_performance_testing.py
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/d4b316e2-5848-4b5c-80d1-9fdeb62933cb)

