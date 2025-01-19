# Example 11: Simulating Network Interruptions

This example demonstrates how to test database operations under simulated network interruptions. It uses a custom MySQL container to introduce random delays and connection errors, ensuring that the application can handle such scenarios gracefully.

---

## Features

- **Custom MySQL Container**: Simulates network instability with random delays and connection errors.
- **Retry Logic**: Implements retry mechanisms for database operations.
- **Transaction Safety**: Ensures that transactions are either fully completed or rolled back in case of failure.
- **Pytest Integration**: Includes a test case to validate fund transfers under network interruptions.

---

## Prerequisites

- Docker installed and running.
- Python 3.8 or higher installed.
- `pip` or `pip3` for installing dependencies.

---

## Directory Structure

```
11_simulating_network_interruptions/
├── 11_network_interruptions.py  # Main test file
├── conftest.py                  # Pytest configuration
├── requirements.txt             # Required Python packages
└── README.md                    # Documentation
```

---

## Installation

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip3 install -r requirements.txt
   ```

---

## Running the Tests

### Direct Execution

You can also run the test directly:
```bash
python 11_simulating_network_interruptions.py -v -s
```
or
```bash
python3 11_simulating_network_interruptions.py -v -s
```

### Using Pytest

Run the test using pytest:
```bash
pytest 11_network_interruptions.py -v -s
```

---

## Expected Output

When running the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/8e4e86f3-b800-48c9-8329-e336b352790e)


---

## Key Takeaways

- **Resilience Testing**: This example demonstrates how to test the resilience of database operations under adverse network conditions.
- **Retry Mechanisms**: Implementing retry logic can help ensure successful operations even in unstable environments.
- **Transaction Safety**: Proper transaction handling ensures data consistency even in the presence of failures.

---
