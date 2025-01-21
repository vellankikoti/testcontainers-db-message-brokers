# **MongoDB with Testcontainers**

## **Overview**
This repository contains a collection of examples demonstrating how to use Testcontainers with MongoDB for testing various scenarios in Python. Each example is accompanied by a detailed `README.md` file to help you understand the concepts and implementation.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
2. [Examples](#examples)
    - [01. Basic CRUD Operations](#01-basic-crud-operations)
    - [02. Indexing and Performance](#02-indexing-and-performance)
    - [03. Transactions](#03-transactions)
    - [04. Aggregation Queries](#04-aggregation-queries)
    - [05. Schema Validation](#05-schema-validation)
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
6. [Contributing](#contributing)

---

## **Getting Started**

### **Prerequisites**
- Python 3.10 or later
- Docker installed and running on your system
- Required Python packages:
  ```bash
  pip install pytest pymongo bcrypt testcontainers
  ```

---

## **Examples**

### 01. Basic CRUD Operations
**Description**: Demonstrates how to perform basic Create, Read, Update, and Delete operations using MongoDB and Testcontainers.  
**File**: `mongodb_example/01_basic_crud_operations.py`  
**README**: [README.md](01_basic_crud_operations/README.md)

### 02. Indexing and Performance
**Description**: Shows how to create and use indexes in MongoDB to improve query performance.  
**File**: `mongodb_example/02_indexing_and_performance.py`  
**README**: [README.md](02_indexing_and_performance/README.md)

### 03. Transactions
**Description**: Implements MongoDB transactions and tests ACID compliance.  
**File**: `mongodb_example/03_transactions.py`  
**README**: [README.md](03_transactions/README.md)

### 04. Aggregation Queries
**Description**: Demonstrates the use of aggregation pipelines for complex data analysis.  
**File**: `mongodb_example/04_aggregation_queries.py`  
**README**: [README.md](04_aggregation_queries/README.md)

### 05. Schema Validation
**Description**: Shows how to enforce schema validation in MongoDB collections.  
**File**: `mongodb_example/05_schema_validation.py`  
**README**: [README.md](05_schema_validation/README.md)

### 06. Simulating Failures
**Description**: Simulates database connection failures and resilience testing.  
**File**: `mongodb_example/06_simulating_failures.py`  
**README**: [README.md](06_simulating_failures/README.md)

### 07. Custom Docker Image
**Description**: Builds and uses a custom Docker image with preloaded MongoDB data.  
**File**: `mongodb_example/07_custom_docker_image.py`  
**README**: [README.md](07_custom_docker_image/README.md)

### 08. Performance Testing
**Description**: Measures performance under high-load scenarios.  
**File**: `mongodb_example/08_performance_testing.py`  
**README**: [README.md](08_performance_testing/README.md)

### 09. Data Migration Testing
**Description**: Validates schema and data migrations.  
**File**: `mongodb_example/09_data_migration_testing.py`  
**README**: [README.md](09_data_migration_testing/README.md)

### 10. Multiple Containers
**Description**: Verifies interactions between MongoDB and another container (e.g., Redis).  
**File**: `mongodb_example/10_multiple_containers.py`  
**README**: [README.md](10_multiple_containers/README.md)

### 11. Simulating Network Interruptions
**Description**: Tests resilience during network disruptions.  
**File**: `mongodb_example/11_simulating_network_interruptions.py`  
**README**: [README.md](11_simulating_network_interruptions/README.md)

### 12. Distributed Transactions
**Description**: Ensures atomicity across services in a distributed system.  
**File**: `mongodb_example/12_distributed_transactions.py`  
**README**: [README.md](12_distributed_transactions/README.md)

### 13. Testing with Mock Services
**Description**: Simulates a mocked payment service for integration tests.  
**File**: `mongodb_example/13_testing_with_mock_services.py`  
**README**: [README.md](13_testing_with_mock_services/README.md)

### 14. Security Testing
**Description**: Validates MongoDB security configurations.  
**File**: `mongodb_example/14_security_testing.py`  
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
   or
    ```bash
   pip3 install -r requirements.txt
   ```

4. Run an example:
   ```bash
   python <example-file>.py
   ```
   or
    ```bash
   python3 <example-file>.py
   ```

6. View the README file for detailed information about each example.

---

## **Troubleshooting**

### Common Issues
1. **Docker Not Running**: Ensure Docker is installed and running on your system.
2. **ModuleNotFoundError**: Install the required Python packages using:
   ```bash
   pip install pytest pymongo bcrypt testcontainers
   ```
3. **Insufficient Resources**: Allocate more CPU and memory to Docker if containers fail to start.

---

## **Conftest.py**
The `conftest.py` file defines shared fixtures for Testcontainers, enabling you to initialize and manage container instances for multiple tests.

---

## **Contributing**
Feel free to contribute by adding new examples, improving existing ones, or reporting issues.

---

