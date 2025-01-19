# Example 6: Simulating Failures (MySQL)

This example demonstrates how to test the system's ability to handle database failures, including connection errors, query execution errors, and transaction rollbacks using MySQL and Testcontainers.

## Overview

The test suite simulates various database failure scenarios to ensure the system handles errors gracefully and maintains data integrity. This is crucial for building robust applications that can recover from unexpected database issues.

---

## Features

- **Connection Failure Testing**: Simulates database connection interruptions.
- **Query Error Handling**: Tests system response to invalid SQL queries.
- **Transaction Rollback Verification**: Ensures data consistency during failed transactions.
- **Automated Recovery**: Demonstrates proper error handling and system recovery.

---

## Prerequisites

- Python 3.8 or higher
- Docker installed and running
- Required Python packages:

```bash
pip install pytest testcontainers sqlalchemy mysql-connector-python
```
or
```bash
pip3 install pytest testcontainers sqlalchemy mysql-connector-python
```
---

## Directory Structure

The directory structure for this example is as follows:
```
mysql_example/
└── 06_simulating_failures/
    ├── 06_simulating_failures.py
    ├── conftest.py
    └── README.md
```

---

## Running the Tests

### 1. Navigate to the Example Directory

```bash
cd mysql_example/06_simulating_failures
```

### 2. Run the Tests

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

![image](https://github.com/user-attachments/assets/c6fe7d98-f3ce-4b38-9a7c-d8943dd52e07)


---

## Test Scenarios

### 1. Connection Failures

- Simulates unexpected database disconnections
- Verifies error handling and connection recovery
- Tests system resilience to network issues

### 2. Query Failures

- Tests handling of invalid SQL queries
- Verifies proper error reporting
- Ensures system stability during query errors

### 3. Transaction Rollbacks

- Simulates failed transactions
- Verifies automatic rollback functionality
- Ensures data consistency after failures

---

## Key Concepts

- **Error Handling**:
  - Proper exception catching and handling
  - Graceful degradation during failures
  - Clear error reporting

- **Data Integrity**:
  - Transaction atomicity
  - Automatic rollbacks
  - Consistent database state

- **Recovery Mechanisms**:
  - Connection retry logic
  - Transaction recovery
  - System state restoration

---

## Common Issues and Solutions

### 1. Docker Issues

- **Problem**: Docker not running
- **Solution**: Start Docker service (use `sudo systemctl start docker`)

### 2. Port Conflicts

- **Problem**: MySQL port already in use
- **Solution**: Stop existing MySQL instances or change the port

### 3. Permission Issues

- **Problem**: Insufficient Docker permissions
- **Solution**: Add user to Docker group or use `sudo`

---

## Best Practices

- **Always Use Transactions**:
  - Wrap critical operations in transactions
  - Enable automatic rollback
  - Maintain data consistency

- **Implement Retry Logic**:
  - Handle temporary failures
  - Use exponential backoff
  - Set appropriate timeouts

- **Log Everything**:
  - Record all failures
  - Track recovery attempts
  - Monitor system health

---

## Future Enhancements

- **Additional Test Scenarios**:
  - Network latency simulation
  - Partial failure scenarios
  - Recovery time measurements

- **Monitoring Integration**:
  - Real-time failure detection
  - Performance impact analysis
  - Recovery metrics collection

- **Advanced Recovery Features**:
  - Custom recovery strategies
  - Failure prediction
  - Automated healing

---
