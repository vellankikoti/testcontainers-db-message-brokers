# Example 13: Testing with Mock Services

This example demonstrates how to test a Kafka-based application using mock services. It focuses on isolating the application components by replacing real services with mocks, allowing for controlled testing scenarios. The example covers:

- Creating mock services to simulate external dependencies.
- Verifying interactions between the application and the mock services.
- Testing various scenarios, including success and failure cases.

## Features

### Mock Service Implementation

- Use libraries like `unittest.mock` or `responses` to create mock services that simulate the behavior of external dependencies.
- Define expected responses for different scenarios (e.g., successful responses, errors).

### Interaction Verification

- Verify that the application interacts correctly with the mock services.
- Ensure that the application handles responses as expected.

### Scenario Testing

- Test various scenarios, including both successful and failed interactions with the mock services.
- Log the results of the tests to confirm the application's behavior.

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

For Mocking:
```bash
pip install responses
```

or
```bash
pip3 install responses
```

### 2. Run the Mock Service Test

Execute the mock service test file using pytest:

For Kafka:
```bash
python -m pytest 13_testing_with_mock_services.py -v -s
```

or
```bash
python3 -m pytest 13_testing_with_mock_services.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/2adf7beb-9c89-4af2-a693-59cce9d47f68)

