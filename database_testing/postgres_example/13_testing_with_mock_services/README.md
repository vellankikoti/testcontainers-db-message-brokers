# Example 13: Testing with Mock Services

## Testing with Mock Services
This example demonstrates how to test interactions with external services by using mock services. Mock services simulate the behavior of real services, allowing you to test your application without relying on the availability or actual implementation of the external service.

---

## Overview
In this example, we test the interaction with a mock payment service. The tests ensure that:
- The application correctly handles successful payment responses.
- The application correctly handles failed payment responses.

By using mock services, we can:
- Simulate different scenarios (e.g., success, failure, timeouts).
- Test edge cases without depending on the real service.
- Speed up testing by avoiding network calls.

---

## Features

### **Mocking External Services**
- Simulates the behavior of an external payment service.
- Uses the `unittest.mock` library to mock HTTP requests.

### **Test Scenarios**
- Successful payment processing.
- Failed payment processing due to insufficient funds.

### **Error Handling**
- Ensures the application handles HTTP errors gracefully.

---

## Code Structure
```
13_testing_with_mock_services/
├── 13_testing_with_mock_services.py  # Main test file
├── conftest.py                       # Pytest configuration for marker registration

```

---

## How to Run the Tests

### 1. Install Dependencies
Install the required Python packages using pip:
```bash
pip install pytest requests
```
Or:
```bash
pip3 install pytest requests
```

### 2. Run the Tests
Run the test file using pytest:
```bash
python -m pytest 13_testing_with_mock_services.py -v -s
```
Or:
```bash
python3 -m pytest 13_testing_with_mock_services.py -v -s
```

---

## Expected Output
When you run the tests, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/2b403c81-cf49-4fa1-8036-d7bc4c02e1f8)

---

## Key Takeaways

### **Mocking External Services**
- Mock services allow you to test your application without relying on real external services.

### **Error Handling**
- The tests ensure that the application handles both success and failure scenarios gracefully.

### **Flexibility**
- Mocking enables you to simulate various scenarios, including edge cases and rare conditions.

### **Speed**
- Tests run faster because they do not make actual network calls.

---

## Common Use Cases

### **Payment Gateways**
- Simulating payment processing for e-commerce applications.

### **Third-Party APIs**
- Testing integrations with external APIs (e.g., weather services, social media APIs).

### **Microservices**
- Testing interactions between microservices in a distributed system.

---

## Future Enhancements

### **Add Timeout Scenarios**
- Simulate network timeouts and ensure the application handles them correctly.

### **Test Retry Logic**
- Add tests for retry mechanisms in case of temporary failures.

### **Expand Mocked Services**
- Mock additional endpoints and test more complex workflows.

---
