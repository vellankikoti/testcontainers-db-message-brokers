# **RabbitMQ with Testcontainers**

## **Overview**
This repository contains a collection of examples demonstrating how to use Testcontainers for testing various scenarios in Python. Each example is accompanied by a detailed README file to help you understand the concepts and implementation.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
2. [Examples](#examples)
    - [01. Basic Guests](#01-basic-guests)
    - [02. Room Management](#02-room-management)
    - [03. Reservations](#03-reservations)
    - [04. Occupancy Report](#04-occupancy-report)
    - [05. Extended Stays](#05-extended-stays)
    - [06. Simulating Failures](#06-simulating-failures)
    - [07. Custom Docker Image](#07-custom-docker-image)
    - [08. Performance Testing](#08-performance-testing)
    - [09. Data Migration Testing](#09-data-migration-testing)
    - [10. Multiple Containers](#10-multiple-containers)
    - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)
    - [12. Distributed Transactions](#12-distributed-transactions)
    - [13. Testing with Mock Services](#13-testing-with-mock-services)
    - [14. Security Testing](#14-security-testing)
3. [How to Run the Examples](#how-to-run-the-examples)
4. [Troubleshooting](#troubleshooting)
5. [Conftest.py](#conftestpy)

---

## **Getting Started**
### **Prerequisites**
- Python 3.10 or later
- Docker installed and running on your system
- Required Python packages:
  ```bash
  pip install testcontainers sqlalchemy requests pytest
  ```

---

## **Examples**

### 01. Basic Guests
**Description**: Demonstrates a basic guest registration system using Testcontainers with a database.  
**File**: `01_basic_guests.py`  
**README**: [README.md](01_basic_guests/README.md)

### 02. Room Management
**Description**: Manages room inventory and pricing in a database.  
**File**: `02_room_management.py`  
**README**: [README.md](02_room_management/README.md)

### 03. Reservations
**Description**: Creates and manages reservations in a database.  
**File**: `03_reservations.py`  
**README**: [README.md](03_reservations/README.md)

### 04. Occupancy Report
**Description**: Generates an occupancy report for the hotel.  
**File**: `04_occupancy_report.py`  
**README**: [README.md](04_occupancy_report/README.md)

### 05. Extended Stays
**Description**: Handles extended stays and calculates total stay duration.  
**File**: `05_extended_stays.py`  
**README**: [README.md](05_extended_stays/README.md)

### 06. Simulating Failures
**Description**: Tests how the system handles various types of database failures.  
**File**: `06_simulating_failures.py`  
**README**: [README.md](06_simulating_failures/README.md)

### 07. Custom Docker Image
**Description**: Demonstrates how to build and use a custom Docker image for RabbitMQ with Testcontainers.  
**File**: `07_custom_docker_image.py`  
**Dockerfile**: `Dockerfile`  
**README**: [README.md](07_custom_docker_image/README.md)

### 08. Performance Testing
**Description**: Simulates high-load scenarios and measures query execution times.  
**File**: `08_performance_testing.py`  
**README**: [README.md](08_performance_testing/README.md)

### 09. Data Migration Testing
**Description**: Tests database migrations and schema changes.  
**File**: `09_data_migration_testing.py`  
**README**: [README.md](09_data_migration_testing/README.md)

### 10. Multiple Containers
**Description**: Tests interactions between multiple containers (e.g., MySQL and Redis).  
**File**: `10_multiple_containers.py`  
**README**: [README.md](10_multiple_containers/README.md)

### 11. Simulating Network Interruptions
**Description**: Tests application resilience during network interruptions.  
**File**: `11_simulating_network_interruptions.py`  
**README**: [README.md](11_simulating_network_interruptions/README.md)

### 12. Distributed Transactions
**Description**: Tests distributed transactions across multiple services (e.g., MySQL and Redis).  
**File**: `12_distributed_transactions.py`  
**README**: [README.md](12_distributed_transactions/README.md)

### 13. Testing with Mock Services
**Description**: Tests application behavior using mock services.  
**File**: `13_testing_with_mock_services.py`  
**README**: [README.md](13_testing_with_mock_services/README.md)

### 14. Security Testing
**Description**: Tests database security configurations, access controls, and encryption.  
**File**: `14_security_testing.py`  
**README**: [README.md](14_security_testing/README.md)

---

## **How to Run the Examples**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run an example:
   ```bash
   python <example-file>.py
   ```

4. View the README file for detailed information about each example.

---

## **Troubleshooting**

### Common Issues
1. **Docker Not Running**: Ensure Docker is installed and running on your system.
2. **ModuleNotFoundError**: Install the required Python packages using:
   ```bash
   pip install testcontainers sqlalchemy requests pytest
   ```
3. **Insufficient Resources**: Allocate more CPU and memory to Docker if containers fail to start.

For more troubleshooting tips, refer to the troubleshooting guide.

---

## **Conftest.py**
The `conftest.py` file is used to define fixtures that can be shared across multiple test files in your examples. It typically contains setup code for Testcontainers, allowing you to initialize and manage container instances for testing purposes. This helps to avoid code duplication and keeps your test files clean and focused on the actual test logic.

For example, in your Testcontainers setup, `conftest.py` might include a fixture that starts a RabbitMQ container, which can then be used in various test cases across different example files.

---

## **Contributing**
Feel free to contribute by adding new examples, improving existing ones, or reporting issues.

---

### Key Updates
- **Added Section for `conftest.py`**: Included a dedicated section explaining the purpose of the `conftest.py` file and how it is used to manage shared fixtures for your tests.
- **Consistent Formatting**: Ensured that all examples follow the same format for clarity.

---
