# Example 11: Simulating Network Interruptions

## Overview
This example demonstrates how to test database resilience by simulating various network issues such as latency, timeouts, and disconnections using Testcontainers and PostgreSQL.

## Features
- Custom container class that simulates network instability.
- Configurable failure rates and latency.
- Retry mechanism for failed transactions.
- Statistical analysis of transaction success rates.
- Network issue simulation including:
  - Random latency.
  - Connection timeouts.
  - Connection drops.

---

## Prerequisites
- Docker installed and running.
- Python 3.8 or higher.
- Required Python packages.

### Installation
Install required packages using pip:
```bash
pip install testcontainers pytest sqlalchemy psycopg2-binary
```
Or:
```bash
pip3 install testcontainers pytest sqlalchemy psycopg2-binary
```

---

## Project Structure
```
11_simulating_network_interruptions/
├── 11_simulating_network_interruptions.py
└── conftest.py
```

---

## Running the Tests
Run the tests using pytest:
```bash
python -m pytest 11_simulating_network_interruptions.py -v -s
```
Or:
```bash
python3 -m pytest 11_simulating_network_interruptions.py -v -s
```

---

## Expected Output

![image](https://github.com/user-attachments/assets/0c5917f8-f6a5-470a-bff3-c817c1bd8df9)


---

## Key Components

### **UnstablePostgresContainer**
- Custom container class extending `PostgresContainer`.
- Configurable failure rate and maximum latency.
- Simulates various network issues using a context manager.

---

## Test Scenarios
- **Connection Timeouts**: Simulates slow or unresponsive network.
- **Random Latency**: Adds random delays to operations.
- **Connection Drops**: Simulates network disconnections.
- **Retry Logic**: Implements robust retry mechanism for failed operations.

---

## Success Criteria
- Minimum **60%** transaction success rate.
- Proper error handling and recovery.
- Successful completion of all test scenarios.

---

## Error Handling
- Implements retry mechanism for failed transactions.
- Catches and handles various SQL and network exceptions.
- Provides detailed error logging and statistics.

---

## Best Practices Demonstrated
- Proper exception handling.
- Retry mechanisms for resilience.
- Statistical tracking of operations.
- Configurable simulation parameters.
- Clean test setup and teardown.

---

## Common Issues and Solutions

### **Docker Not Running**
**Solution**: Start the Docker daemon.

### **Port Conflicts**
**Solution**: Ensure no other services are using PostgreSQL's default port (5432).

### **Permission Issues**
**Solution**: Run Docker commands with appropriate permissions.

---

## Performance Considerations
- Tests may take longer due to simulated delays.
- Adjust `failure_rate` and `max_latency` parameters for different scenarios.
- Consider system resources when running multiple tests.
