# **Redis Testing with Testcontainers 🚀**  

Welcome to the **Redis Testing** section! This guide provides a **comprehensive overview** of how to use **Testcontainers** with **Redis**. It includes **real-world test cases** to validate **message integrity, persistence, resilience, and performance** using Redis.

---

## **Table of Contents**  

- [Overview](#overview)  
- [Getting Started](#getting-started)  
- [Redis Testing](#redis-testing)  
- [Examples](#examples)  
  - [01. Basic Publish/Subscribe Operations](#01-basic-publishsubscribe-operations)  
  - [02. Message Persistence](#02-message-persistence)  
  - [03. Data Integrity Testing](#03-data-integrity-testing)  
  - [04. Performance Testing](#04-performance-testing)  
  - [05. Field Constraints & Index Testing](#05-field-constraints--index-testing)  
  - [06. Simulating Failures](#06-simulating-failures)  
  - [07. Custom Docker Image](#07-custom-docker-image)  
  - [08. Load Testing](#08-load-testing)  
  - [09. Data Migration Testing](#09-data-migration-testing)  
  - [10. Multiple Instances](#10-multiple-instances)  
  - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)  
  - [12. Distributed Transactions](#12-distributed-transactions)  
  - [13. Testing with Mock Services](#13-testing-with-mock-services)  
  - [14. Security Testing](#14-security-testing)  
- [How to Run the Examples](#how-to-run-the-examples)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  

---

## **Overview**  

This repository provides **real-world Redis testing examples** using **Testcontainers** in Python. Each test case follows a **structured approach**, from **basic publish/subscribe messaging** to **advanced resilience, performance, and security testing**.

---

## **Getting Started**  

### **Prerequisites**  

- **Python 3.10** or later  
- **Docker installed and running** on your system  
- Install required Python packages:  
  ```bash
  pip install pytest redis testcontainers
  ```

---

## **Redis Testing**  

Redis is a **high-performance, in-memory data structure store** that can be used as a **database, cache, and message broker**. This section provides **Redis testing scenarios** using **Testcontainers** for containerized, automated testing.

---

## **Examples**  

### **01. Basic Publish/Subscribe Operations**  
- **Description**: Tests Redis’ basic **publish-subscribe mechanism**.  
- **File**: `redis_example/01_basic_pub_sub.py`  
- **README**: [README.md](redis_example/01_basic_pub_sub/README.md)  

### **02. Message Persistence**  
- **Description**: Ensures **messages persist** across Redis restarts.  
- **File**: `redis_example/02_message_persistence.py`  
- **README**: [README.md](redis_example/02_message_persistence/README.md)  

### **03. Data Integrity Testing**  
- **Description**: Verifies **message ordering, durability, and duplication**.  
- **File**: `redis_example/03_data_integrity_testing.py`  
- **README**: [README.md](redis_example/03_data_integrity_testing/README.md)  

### **04. Performance Testing**  
- **Description**: Measures **Redis throughput and latency** under high-load scenarios.  
- **File**: `redis_example/04_performance_testing.py`  
- **README**: [README.md](redis_example/04_performance_testing/README.md)  

### **05. Field Constraints & Index Testing**  
- **Description**: Tests **Redis expiry policies, key constraints, and indexing mechanisms**.  
- **File**: `redis_example/05_field_constraints_and_indexes.py`  
- **README**: [README.md](redis_example/05_field_constraints_and_indexes/README.md)  

### **06. Simulating Failures**  
- **Description**: Simulates **Redis node crashes and network failures**.  
- **File**: `redis_example/06_simulating_failures.py`  
- **README**: [README.md](redis_example/06_simulating_failures/README.md)  

### **07. Custom Docker Image**  
- **Description**: Creates and tests a **custom Redis Docker image** with configurations.  
- **File**: `redis_example/07_custom_docker_image.py`  
- **Dockerfile**: `redis_example/Dockerfile`  
- **README**: [README.md](redis_example/07_custom_docker_image/README.md)  

### **08. Load Testing**  
- **Description**: Simulates **high-throughput workloads** to benchmark Redis performance.  
- **File**: `redis_example/08_load_testing.py`  
- **README**: [README.md](redis_example/08_load_testing/README.md)  

### **09. Data Migration Testing**  
- **Description**: Uses Redis for **data migration across different environments**.  
- **File**: `redis_example/09_data_migration_testing.py`  
- **README**: [README.md](redis_example/09_data_migration_testing/README.md)  

### **10. Multiple Instances**  
- **Description**: Configures and tests **multiple Redis instances** for horizontal scaling.  
- **File**: `redis_example/10_multiple_instances.py`  
- **README**: [README.md](redis_example/10_multiple_instances/README.md)  

### **11. Simulating Network Interruptions**  
- **Description**: Tests Redis’ **fault tolerance against network disruptions**.  
- **File**: `redis_example/11_simulating_network_interruptions.py`  
- **README**: [README.md](redis_example/11_simulating_network_interruptions/README.md)  

### **12. Distributed Transactions**  
- **Description**: Implements **Redis transactions across multiple operations**.  
- **File**: `redis_example/12_distributed_transactions.py`  
- **README**: [README.md](redis_example/12_distributed_transactions/README.md)  

### **13. Testing with Mock Services**  
- **Description**: Mocks **external services interacting with Redis**.  
- **File**: `redis_example/13_testing_with_mock_services.py`  
- **README**: [README.md](redis_example/13_testing_with_mock_services/README.md)  

### **14. Security Testing**  
- **Description**: Tests Redis’ **authentication, encryption, and ACL rules**.  
- **File**: `redis_example/14_security_testing.py`  
- **README**: [README.md](redis_example/14_security_testing/README.md)  

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
   python3 -m pytest <example-file>.py -v -s
   ```  

4. **Check the `README.md` file inside each example folder** for further details.  

---

## **Troubleshooting**  

### **Common Issues and Fixes**  

- **Docker Not Running**  
  ```bash
  docker ps
  ```  

- **Port Conflicts**  
  ```bash
  docker ps | grep 6379  # Redis
  ```  

- **Missing Dependencies**  
  ```bash
  pip install -r requirements.txt
  ```  

---

## **Contributing**  

- Feel free to **add new examples, improve existing ones, or report issues**.  
- Contributions are welcome in **writing documentation, adding test cases, or optimizing performance tests**.  

---

## **🚀 Happy Testing with Redis and Testcontainers!** 🎉  

---
