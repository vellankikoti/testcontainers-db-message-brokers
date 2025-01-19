# Example 10: Multiple Containers

This example demonstrates how to test interactions between a MySQL database and a Redis cache using Testcontainers.

## Features

- **Multiple Container Setup**: Run and manage MySQL and Redis containers simultaneously.
- **Data Synchronization**: Test data synchronization between the database and the cache.
- **Integration Testing**: Validate the interaction between the database and the cache.

## Prerequisites

- **Docker**: Ensure Docker is installed and running.
- **Python 3.7+**: Required for running the tests.
- **pip**: Python package manager for installing dependencies.

## Installation

1. Clone the repository or navigate to the `10_multiple_containers` directory.
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
10_multiple_containers/
├── 10_multiple_containers.py   # Main test file
├── conftest.py                 # Pytest configuration
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Running the Tests

1. Run the tests:
   ```bash
   python 10_multiple_containers.py -v -s
   ```
   or
   ```bash
   python3 10_multiple_containers.py -v -s
   ```

   - `-v`: Enables verbose output.
   - `-s`: Displays print statements in the console.

## Expected Output

If the tests run successfully, you should see output similar to this:

![image](https://github.com/user-attachments/assets/8c60d5c2-12cd-43cb-be6d-cf290a36b9bc)


## Key Takeaways

- **Integration Testing**: Validates the interaction between multiple services in a controlled environment.
- **Data Synchronization**: Ensures data consistency between the database and the cache.
- **Testcontainers**: Provides an isolated and reproducible environment for testing.

