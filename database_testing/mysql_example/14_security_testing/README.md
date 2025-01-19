# Example 14: Security Testing

This example demonstrates how to test the security aspects of an application, including:

- **SQL Injection Prevention**
- **Password Hashing and Validation**
- **Rate Limiting**
- **Input Validation**
- **Account Lockout Mechanisms**
- **Session Management**
- **Audit Logging**

---

## Features

- **Password Security**: Validates password strength and securely hashes passwords using SHA-256.
- **Rate Limiting**: Prevents abuse by limiting the number of requests from a single IP address within a time window.
- **Account Lockout**: Locks user accounts after multiple failed login attempts.
- **Session Management**: Creates and manages user sessions with expiration times.
- **Audit Logging**: Logs security-related events such as login attempts and account lockouts.
- **SQL Injection Prevention**: Uses parameterized queries to prevent SQL injection attacks.

---

## Prerequisites

- Docker installed and running.
- Python 3.8 or higher installed.
- `pip` or `pip3` for installing dependencies.

---

## Directory Structure

```
14_security_testing/
├── 14_security_testing.py  # Main test file
├── conftest.py             # Pytest configuration
├── requirements.txt        # Required Python packages
└── README.md               # Documentation
```

---

## Installation

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Tests

### Direct Execution

You can also run the tests directly:
```bash
python 14_security_testing.py
```
or
```bash
python3 14_security_testing.py
```

### Using Pytest

Run the tests using pytest:
```bash
pytest 14_security_testing.py -v -s
```

---

## Expected Output

When running the tests, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/83cdce86-5a7d-4d62-8b7f-2dbce9eb4e13)

---

## Key Takeaways

- **Password Security**: Always validate password strength and store passwords securely using hashing algorithms.
- **Rate Limiting**: Implement rate limiting to prevent abuse and protect your application from brute-force attacks.
- **Account Lockout**: Lock accounts temporarily after multiple failed login attempts to prevent unauthorized access.
- **SQL Injection Prevention**: Use parameterized queries to prevent SQL injection attacks.
- **Audit Logging**: Maintain logs of security-related events for monitoring and debugging.

---
