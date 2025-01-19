# Example 6: Simulating Failures (MongoDB)

This example demonstrates how to use Testcontainers to test the resilience of a MongoDB-based system by simulating database failures. It covers:

- Handling connection failures.
- Testing query execution errors.
- Simulating transaction rollbacks.
- Validating error handling mechanisms.

---

## Overview

The test simulates a hotel management system under failure scenarios. It performs the following operations:

1. **Connection Failures**: Simulate database connection issues and validate recovery mechanisms.
2. **Query Errors**: Test how the system handles invalid or failed queries.
3. **Transaction Rollbacks**: Ensure data consistency during partial failures.
4. **Error Logging**: Validate proper logging of errors for debugging.

---

## Features

### Failure Simulation

- Simulate database connection interruptions.
- Test invalid query execution.
- Force transaction rollbacks.

### Error Handling

- Validate error messages and codes.
- Ensure proper exception handling.
- Test retry mechanisms for transient failures.

### Data Consistency

- Ensure no partial updates during failures.
- Validate rollback mechanisms.
- Test atomicity of operations.

---

## How to Run the Test

### Build the Docker image

```bash
docker compose up -d
```

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 06_simulating_failures.py -v -s
```

or

```bash
python3 -m pytest 06_simulating_failures.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/dce58eda-360d-4de8-9033-6f6253e5e940)

---

## Code Walkthrough

### 1. Failure Scenarios

- **Connection Failure**: Simulate a database connection interruption and validate recovery.
- **Query Execution Error**: Execute invalid queries and validate error handling.
- **Transaction Rollback**: Simulate partial failures and ensure rollback.
- **Error Logging**: Validate proper logging of errors for debugging.

### 2. Key Operations

- Simulate connection interruptions.
- Execute invalid queries.
- Force transaction rollbacks.
- Log errors for debugging.

### 3. Test Cases

- Connection failure handling.
- Query execution error validation.
- Transaction rollback testing.
- Error logging verification.

---

## Key Takeaways

### MongoDB Benefits

- Flexible schema for error simulation.
- Efficient transaction handling.
- Easy error logging.
- Resilience testing.

### Testing Practices

- Comprehensive failure scenarios.
- Edge case handling.
- Clear test organization.
- Proper cleanup.

### Resilience Testing

- Robust error handling.
- Data consistency validation.
- Recovery mechanism testing.
- Logging and debugging.

---

## Common Issues and Solutions

### 1. Connection Failures

- Implement retry mechanisms.
- Use connection pooling.
- Handle transient errors.

### 2. Query Errors

- Validate query syntax.
- Handle invalid queries gracefully.
- Log detailed error messages.

### 3. Transaction Rollbacks

- Ensure atomic operations.
- Validate rollback mechanisms.
- Test partial failures.

---

## Future Enhancements

### Planned Features

- Advanced failure simulations.
- Real-time monitoring of failures.
- Automated recovery mechanisms.
- Integration with alerting systems.

### Testing Improvements

- Load testing under failure scenarios.
- Concurrent failure simulations.
- Extended rollback scenarios.
- Complex error handling.

---
