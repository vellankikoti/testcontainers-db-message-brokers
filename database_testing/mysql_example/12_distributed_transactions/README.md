# Example 12: Distributed Transactions

This example demonstrates how to test distributed transactions across multiple MySQL databases using a two-phase commit protocol simulation. It ensures that operations across different databases are coordinated and can be rolled back in case of failures.

---

## Features

- **Distributed Transactions**: Manages transactions across multiple databases to ensure data consistency.
- **Two-Phase Commit Protocol**: Simulates the two-phase commit process for distributed transactions.
- **Error Handling**: Tests rollback functionality in case of errors during transaction processing.
- **Pytest Integration**: Includes test cases to validate distributed transaction processing.

---

## Prerequisites

- Docker installed and running.
- Python 3.8 or higher installed.
- `pip` or `pip3` for installing dependencies.

---

## Directory Structure

```
12_distributed_transactions/
├── 12_distributed_transactions.py  # Main test file
├── conftest.py                     # Pytest configuration
├── requirements.txt                # Required Python packages
└── README.md                       # Documentation
```

---

## Installation

1. Clone the repository or navigate to the example directory:
   ```bash
   cd 12_distributed_transactions
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Tests

### Direct Execution

You can also run the test directly:
```bash
python 12_distributed_transactions.py
```
or
```bash
python3 12_distributed_transactions.py
```

### Using Pytest

Run the test using pytest:
```bash
pytest 12_distributed_transactions.py -v -s
```


---

## Expected Output

When running the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/7c8dc8b7-a5a8-4795-b8f4-fc3d20241996)

---

## Key Takeaways

- **Data Consistency**: This example demonstrates how to ensure data consistency across multiple databases using distributed transactions.
- **Error Handling**: Proper error handling is critical to maintaining the integrity of distributed operations.
- **Two-Phase Commit**: Understanding the two-phase commit protocol is essential for managing distributed transactions effectively.

---
