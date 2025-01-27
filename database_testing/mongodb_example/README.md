# **MongoDB with Testcontainers**

## **Overview**
This repository contains a collection of examples demonstrating how to use **Testcontainers with MongoDB** for testing various scenarios in Python. Each example is accompanied by a **detailed `README.md` file** to help you understand the concepts and implementation.

---

## **Table of Contents**
1. [Getting Started](#getting-started)
2. [Examples](#examples)
    - [01. Basic CRUD Operations](#01-basic-crud-operations)
    - [02. Indexing and Performance](#02-indexing-and-performance)
    - [03. Data Integrity Testing](#03-data-integrity-testing)
    - [04. Aggregation Queries](#04-aggregation-queries)
    - [05. Field Constraints & Index Testing](#05-field-constraints--index-testing)
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
5. [Best Practices](#best-practices)
6. [Conftest.py](#conftestpy)
7. [Contributing](#contributing)

---

## **Getting Started**

### **Prerequisites**
- **Python 3.10** or later
- **Docker** installed and running on your system
- Required Python packages:
  ```bash
  pip install pytest pymongo bcrypt testcontainers
  ```

---

## **Examples**

### **01. Basic CRUD Operations**
**File**: `mongodb_example/01_basic_crud_operations.py`  
**Description**: Demonstrates how to perform basic **Create, Read, Update, and Delete (CRUD) operations** using MongoDB and Testcontainers.  
**README**: [README.md](01_basic_crud_operations/README.md)

### **02. Indexing and Performance**
**File**: `mongodb_example/02_indexing_and_performance.py`  
**Description**: Shows how to **create and use indexes** in MongoDB to improve query performance.  
**README**: [README.md](02_indexing_and_performance/README.md)

### **03. Data Integrity Testing** (Updated ✅)
**File**: `mongodb_example/03_data_integrity_testing.py`  
**Description**: Ensures MongoDB **enforces data integrity** by testing:  
- **Unique Constraints**: Prevents duplicate records.  
- **Field Validation**: Ensures required fields exist and match expected types.  
- **Atomic Transactions**: Ensures multiple operations succeed or fail together.  
**README**: [README.md](03_data_integrity_testing/README.md)

### **04. Aggregation Queries**
**File**: `mongodb_example/04_aggregation_queries.py`  
**Description**: Demonstrates the use of **aggregation pipelines** for complex data analysis.  
**README**: [README.md](04_aggregation_queries/README.md)

### **05. Field Constraints & Index Testing** (Updated ✅)
**File**: `mongodb_example/05_field_constraints_and_indexes.py`  
**Description**: Tests **MongoDB constraints and indexing**:
- **Field Constraints**: Enforces required fields and correct data types.
- **Unique Indexes**: Ensures duplicate values are not inserted.
- **Index Performance**: Verifies indexed queries execute efficiently.
**README**: [README.md](05_field_constraints_and_indexes/README.md)

### **06. Simulating Failures**
**File**: `mongodb_example/06_simulating_failures.py`  
**Description**: Tests **database resilience** by simulating **connection failures**.  
**README**: [README.md](06_simulating_failures/README.md)

### **07. Custom Docker Image**
**File**: `mongodb_example/07_custom_docker_image.py`  
**Description**: Builds and uses a **custom Docker image** with preloaded MongoDB data.  
**README**: [README.md](07_custom_docker_image/README.md)

### **08. Performance Testing**
**File**: `mongodb_example/08_performance_testing.py`  
**Description**: Measures **performance under high-load scenarios**.  
**README**: [README.md](08_performance_testing/README.md)

### **09. Data Migration Testing**
**File**: `mongodb_example/09_data_migration_testing.py`  
**Description**: Validates **schema and data migrations** in MongoDB.  
**README**: [README.md](09_data_migration_testing/README.md)

### **10. Multiple Containers**
**File**: `mongodb_example/10_multiple_containers.py`  
**Description**: Verifies **interactions between MongoDB and another container (e.g., Redis, Kafka, RabbitMQ)**.  
**README**: [README.md](10_multiple_containers/README.md)

### **11. Simulating Network Interruptions**
**File**: `mongodb_example/11_simulating_network_interruptions.py`  
**Description**: Tests **MongoDB resilience** during **network disruptions**.  
**README**: [README.md](11_simulating_network_interruptions/README.md)

### **12. Distributed Transactions**
**File**: `mongodb_example/12_distributed_transactions.py`  
**Description**: Ensures **atomicity across multiple services** using **multi-document transactions**.  
**README**: [README.md](12_distributed_transactions/README.md)

### **13. Testing with Mock Services**
**File**: `mongodb_example/13_testing_with_mock_services.py`  
**Description**: Simulates **external APIs for integration testing**.  
**README**: [README.md](13_testing_with_mock_services/README.md)

### **14. Security Testing**
**File**: `mongodb_example/14_security_testing.py`  
**Description**: Tests **security configurations** such as authentication, authorization, and **NoSQL injection vulnerabilities**.  
**README**: [README.md](14_security_testing/README.md)

---

## **How to Run the Examples**

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run an example**:
   ```bash
   python -m pytest <example-file>.py -v
   ```

---

## **Troubleshooting**

### Common Issues and Fixes

- **Docker Not Running**
  ```bash
  docker ps
  ```

- **MongoDB Port Conflicts**
  ```bash
  docker ps | grep 27017
  ```

- **Missing Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

---

## **Best Practices**

- **Use Indexing Efficiently**: Index frequently queried fields to improve performance.
- **Validate Data at Insertion**: Use **schema validation** to enforce correct field types.
- **Simulate Real-World Failures**: Test with **network failures and replica sets** for robustness.
- **Ensure Atomic Transactions**: Multi-document transactions help maintain data consistency.

---

## **Conftest.py**
The `conftest.py` file defines shared fixtures for **Testcontainers**, enabling you to **initialize and manage MongoDB instances** dynamically.

---

## **Contributing**
Feel free to contribute by **adding new examples**, **improving existing ones**, or **reporting issues**.

---

## **🚀 Happy Testing!**

---
