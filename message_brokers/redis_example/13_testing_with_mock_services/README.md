# Example 13: Testing with Mock Services

This example demonstrates how to use mock services to test the reservation system using Redis as the data store. It focuses on isolating the system's components during testing to ensure that each part functions correctly without relying on external services. The example covers:

- Setting up mock services for testing.
- Simulating responses from external dependencies.
- Verifying the behavior of the reservation system under various scenarios.

## Features

### Mock Service Implementation

- Create mock services to simulate external dependencies.
- Use libraries like `unittest.mock` or `responses` to mock HTTP requests and responses.

### Error Handling

- Handle errors during testing with mock services.
- Provide appropriate error messages for failed tests or unexpected behavior.

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

### 2. Run the Mock Service Tests

Execute the test file using pytest:

For Redis:
```bash
python -m pytest 13_testing_with_mock_services.py -v -s
```

or
```bash
python3 -m pytest 13_testing_with_mock_services.py -v -s
```

### Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/8f364873-6e8f-49c6-8af5-fc608628e95e)

