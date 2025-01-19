# Example 8: Performance Testing

This example demonstrates how to perform database performance testing using Python, pytest, and Testcontainers. It focuses on measuring query execution times, calculating performance metrics, and setting performance thresholds to ensure efficient database operations.

## Features

- Measure execution time for different types of SQL queries.
- Calculate performance statistics (min, max, average, median).
- Test various query types (SELECT, INSERT, JOIN).
- Handle multiple test iterations for reliable metrics.
- Custom performance metrics tracking.

## Prerequisites

- **Docker**: Ensure Docker is installed and running.
- **Python 3.7+**: Required for running the tests.
- **pip**: Python package manager for installing dependencies.

## Installation

1. Clone the repository or navigate to the `08_performance_testing` directory.
2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```
## Directory Structure

```
08_performance_testing/
├── 08_performance_testing.py   # Main test file
├── conftest.py                 # Pytest configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```
---

## Running the Tests

**Run the tests using pytest:**

```bash
pytest 08_performance_testing.py -v -s
```

- `-v`: Enables verbose output.
- `-s`: Displays print statements in the console.

Alternatively, you can run the tests directly with Python:
```bash
python 08_performance_testing.py
```
or
```bash
python3 08_performance_testing.py
```

## Test Cases

1. **SELECT Performance Test**  
   Measures the performance of basic SELECT queries.  
   - Calculates statistics over multiple iterations.
   - Verifies that the average query time is under 1 second.

2. **INSERT Performance Test**  
   Tests the performance of INSERT operations.  
   - Measures the time taken to insert new records.
   - Ensures the average insert time is under 0.5 seconds.

3. **JOIN Performance Test**  
   Evaluates the performance of JOIN operations.  
   - Measures the execution time of complex queries.
   - Verifies that the average join query time is under 1.5 seconds.

## Expected Output

If the tests run successfully, you should see output similar to this:

![image](https://github.com/user-attachments/assets/9b58d64c-4eba-4fd3-b756-bcac4b36e202)


## Key Takeaways

- **Performance Testing**: Helps identify slow queries and optimize them.
- **Query Optimization**: Use indexes and proper query design to improve performance.
- **Testcontainers**: Makes it easy to test database performance in isolated environments.
- **Statistical Analysis**: Provides insights into query performance over multiple iterations.

