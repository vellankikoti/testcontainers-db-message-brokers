# Example 13: Testing with Mock Services

This example demonstrates how to test applications that interact with external services using mock services. Mock services allow you to simulate different scenarios and responses from external APIs, enabling you to test your application without relying on real external services.

---

## Features

- **Mock Services**: Simulates external services like payment gateways for testing.
- **Error Simulation**: Tests application behavior when external services fail.
- **Delayed Responses**: Simulates slow responses from external services to test timeout handling.
- **Database Integration**: Verifies that payment records are stored correctly in the database.
- **Pytest Integration**: Includes test cases to validate application behavior under different scenarios.

---

## Prerequisites

- Docker installed and running.
- Python 3.8 or higher installed.
- `pip` or `pip3` for installing dependencies.

---

## Directory Structure

```
13_testing_with_mock_services/
├── 13_testing_with_mock_services.py  # Main test file
├── conftest.py                       # Pytest configuration
├── requirements.txt                  # Required Python packages
└── README.md                         # Documentation
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
python 13_testing_with_mock_services.py
```
or
```bash
python3 13_testing_with_mock_services.py
```
### Using Pytest

Run the test using pytest:
```bash
pytest 13_testing_with_mock_services.py -v -s
```

---

## Expected Output

When running the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/f0fadbc4-47de-4dad-95a9-8ec454d72293)


---

## Key Takeaways

- **Mock Services**: Mocking external services allows you to test your application without relying on real APIs, making tests faster and more reliable.
- **Error Handling**: This example demonstrates how to handle errors from external services gracefully.
- **Database Integration**: Verifies that application logic correctly interacts with the database, even when external services fail.

---
