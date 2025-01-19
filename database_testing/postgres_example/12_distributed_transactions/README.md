# Example 12: Distributed Transactions

## Distributed Transactions Testing
This example demonstrates how to test distributed transactions across multiple databases using the **two-phase commit protocol**. Distributed transactions are critical for ensuring data consistency when multiple databases are involved in a single logical operation.

---

## Overview
In this example, we simulate a distributed transaction involving two PostgreSQL databases:

1. **Orders Database**: Manages customer orders.
2. **Inventory Database**: Manages product inventory.

The test ensures that:
- Both databases are prepared for the transaction (**Phase 1: Prepare**).
- The transaction is either committed to both databases or rolled back entirely (**Phase 2: Commit or Rollback**).

---

## Features

### **Two-Phase Commit Protocol**
- **Prepare Phase**: Ensures both databases are ready for the transaction.
- **Commit Phase**: Finalizes the transaction in both databases.
- **Rollback**: Reverts changes in case of failure.

### **Simulated Failure**
- Tests the rollback mechanism when a failure occurs before the commit phase.

### **Data Integrity**
- Ensures that no partial changes are committed to the databases.

---

## Code Structure
```
12_distributed_transactions/
├── 12_distributed_transactions.py  # Main test file
├── conftest.py                     # Pytest configuration for marker registration

```

---

## How to Run the Tests

### 1. Install Dependencies
```bash
pip install testcontainers pytest sqlalchemy psycopg2-binary
```
Or:
```bash
pip3 install testcontainers pytest sqlalchemy psycopg2-binary
```

### 2. Run the Tests
Run the test file using pytest:
```bash
python -m pytest 12_distributed_transactions.py -v -s
```
Or:
```bash
python3 -m pytest 12_distributed_transactions.py -v -s
```

---

## Expected Output
When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/2269cc37-2370-47f4-af47-ab154ebb035c)


---

## Key Takeaways

### **Two-Phase Commit Protocol**
- Demonstrates the two-phase commit protocol, ensuring that distributed transactions are either fully committed or fully rolled back.

### **Data Consistency**
- Ensures that no partial changes are committed to either database in case of a failure.

### **Error Handling**
- Tests the rollback mechanism to ensure proper recovery from failures.

### **Scalability**
- This approach can be extended to more than two databases or other types of distributed systems.

---

## Common Use Cases

### **E-commerce Systems**
- Ensures consistency between order processing and inventory management.

### **Banking Systems**
- Coordinates transactions across multiple accounts or financial institutions.

### **Microservices Architecture**
- Manages distributed transactions across multiple services with independent databases.

---

## Future Enhancements

### **Add More Failure Scenarios**
- Simulate network interruptions or database crashes during the transaction.

### **Support for Other Databases**
- Extend the test to include other database systems like MySQL or MongoDB.

### **Logging and Monitoring**
- Add detailed logging and monitoring for distributed transactions.

---
