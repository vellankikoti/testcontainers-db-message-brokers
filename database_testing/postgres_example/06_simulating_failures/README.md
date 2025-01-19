# Example 6: Simulating Failures

## Overview
This example demonstrates how to test database failure scenarios in a controlled environment using Python, SQLAlchemy, and TestContainers. It shows how to properly handle various database failures while maintaining data integrity.

---

## Key Concepts

### Failure Scenarios Tested
- Query execution failures.
- Transaction rollbacks.
- Connection error handling.
- Data integrity verification.

### Testing Approach
- Controlled failure simulation.
- Proper transaction management.
- Verification of rollback effectiveness.
- Clean state management.

---

## Code Structure

### Main Components

#### Database Setup
```python
def setup_database(connection):
    """Creates transactions table and establishes schema and constraints."""
```

#### Sample Data Management
```python
def insert_sample_data(connection):
    """Inserts test transactions and sets up the initial state."""
```

#### Failure Simulations
```python
def simulate_query_failure(connection):
    """Tests invalid SQL queries."""
```

```python
def simulate_transaction_failure(connection):
    """Tests transaction rollbacks."""
```

---

## Running the Tests

### Prerequisites
- **Python 3.8+**
- **Docker** installed and running.
- Required packages:
  ```bash
  pip install pytest testcontainers sqlalchemy psycopg2-binary
  ```

### Execution
Run the tests using:
```bash
python -m pytest 06_simulating_failures.py -v
```

---

## Expected Output
![image](https://github.com/user-attachments/assets/9ed0ba14-96ca-48e9-8856-ca669b71a5c8)


---

## Key Takeaways

### Error Handling Best Practices
- Always use `try-except` blocks for database operations.
- Properly manage transaction states.
- Verify rollbacks are successful.
- Clean up resources after failures.

### Transaction Management
- Explicit transaction control.
- Proper rollback handling.
- State verification after rollbacks.
- Clear transaction boundaries.

### Data Integrity
- Verify failed operations don't persist data.
- Maintain database consistency.
- Handle cleanup after failures.
- Validate expected state.

---

## Common Pitfalls

### Transaction State Management
- Not properly rolling back failed transactions.
- Nested transaction issues.
- Missing commit/rollback calls.
- Unclear transaction boundaries.

### Resource Cleanup
- Not closing connections.
- Leaving transactions open.
- Memory leaks.
- Resource exhaustion.

---

## Debugging Tips

### Common Issues
- Transaction already in progress.
- Failed rollbacks.
- Connection pooling issues.
- Resource cleanup failures.

### Solutions
- Use explicit transaction management.
- Verify connection states.
- Implement proper cleanup.
- Monitor resource usage.

---

## Future Enhancements

### Additional Test Scenarios
- Network failures.
- Deadlock situations.
- Concurrent transaction issues.
- Connection pool exhaustion.

### Improvements
- More detailed error reporting.
- Performance metrics.
- Resource usage monitoring.
- Extended failure scenarios.

---

## Related Documentation
- [SQLAlchemy Transaction Management](https://docs.sqlalchemy.org/en/20/core/transactions.html)
- [pytest Documentation](https://docs.pytest.org/en/latest/)
- [TestContainers Python](https://testcontainers-python.readthedocs.io/)

