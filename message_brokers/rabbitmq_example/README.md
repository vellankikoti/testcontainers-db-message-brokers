# **RabbitMQ Testing with Testcontainers 🐰**  

Welcome to the **RabbitMQ Testing** section! This guide provides a **comprehensive overview** of how to use **Testcontainers** with **RabbitMQ**. It includes **real-world test cases** to validate **message integrity, persistence, resilience, and performance** using RabbitMQ.

---

## **Table of Contents**  

- [Overview](#overview)  
- [Getting Started](#getting-started)  
- [RabbitMQ Testing](#rabbitmq-testing)  
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
  - [10. Multiple Queues](#10-multiple-queues)  
  - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)  
  - [12. Distributed Transactions](#12-distributed-transactions)  
  - [13. Testing with Mock Services](#13-testing-with-mock-services)  
  - [14. Security Testing](#14-security-testing)  
- [How to Run the Examples](#how-to-run-the-examples)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  

---

## **Overview**  

This repository provides **real-world RabbitMQ testing examples** using **Testcontainers** in Python. Each test case follows a **structured approach**, from **basic publish/subscribe messaging** to **advanced resilience, performance, and security testing**.

---

## **Getting Started**  

### **Prerequisites**  

- **Python 3.10** or later  
- **Docker installed and running** on your system  
- Install required Python packages:  
  ```bash
  pip install pytest pika testcontainers
  ```

---

## **RabbitMQ Testing**  

RabbitMQ is a **widely used message broker** that implements the **Advanced Message Queuing Protocol (AMQP)**. This section provides **RabbitMQ testing scenarios** using **Testcontainers** for containerized, automated testing.

---

## **Examples**  

### **01. Basic Publish/Subscribe Operations**  
- **Description**: Tests RabbitMQ’s basic **publish-subscribe mechanism**.  
- **File**: `rabbitmq_example/01_basic_pub_sub.py`  
- **README**: [README.md](rabbitmq_example/01_basic_pub_sub/README.md)  

### **02. Message Persistence**  
- **Description**: Ensures **messages persist** across RabbitMQ restarts.  
- **File**: `rabbitmq_example/02_message_persistence.py`  
- **README**: [README.md](rabbitmq_example/02_message_persistence/README.md)  

### **03. Data Integrity Testing**  
- **Description**: Verifies **message order, delivery guarantees, and duplicate prevention**.  
- **File**: `rabbitmq_example/03_data_integrity_testing.py`  
- **README**: [README.md](rabbitmq_example/03_data_integrity_testing/README.md)  

### **04. Performance Testing**  
- **Description**: Measures **RabbitMQ throughput and latency** under high-load scenarios.  
- **File**: `rabbitmq_example/04_performance_testing.py`  
- **README**: [README.md](rabbitmq_example/04_performance_testing/README.md)  

### **05. Field Constraints & Index Testing**  
- **Description**: Tests **queue durability, message TTL, and dead-letter exchanges**.  
- **File**: `rabbitmq_example/05_field_constraints_and_indexes.py`  
- **README**: [README.md](rabbitmq_example/05_field_constraints_and_indexes/README.md)  

### **06. Simulating Failures**  
- **Description**: Simulates **RabbitMQ node failures and queue failures**.  
- **File**: `rabbitmq_example/06_simulating_failures.py`  
- **README**: [README.md](rabbitmq_example/06_simulating_failures/README.md)  

### **07. Custom Docker Image**  
- **Description**: Creates and tests a **custom RabbitMQ Docker image** with configurations.  
- **File**: `rabbitmq_example/07_custom_docker_image.py`  
- **Dockerfile**: `rabbitmq_example/Dockerfile`  
- **README**: [README.md](rabbitmq_example/07_custom_docker_image/README.md)  

### **08. Load Testing**  
- **Description**: Simulates **high-throughput workloads** to benchmark RabbitMQ performance.  
- **File**: `rabbitmq_example/08_load_testing.py`  
- **README**: [README.md](rabbitmq_example/08_load_testing/README.md)  

### **09. Data Migration Testing**  
- **Description**: Uses RabbitMQ for **data migration across different systems**.  
- **File**: `rabbitmq_example/09_data_migration_testing.py`  
- **README**: [README.md](rabbitmq_example/09_data_migration_testing/README.md)  

### **10. Multiple Queues**  
- **Description**: Configures and tests **RabbitMQ multi-queue setups**.  
- **File**: `rabbitmq_example/10_multiple_queues.py`  
- **README**: [README.md](rabbitmq_example/10_multiple_queues/README.md)  

### **11. Simulating Network Interruptions**  
- **Description**: Tests RabbitMQ’s **fault tolerance against network disruptions**.  
- **File**: `rabbitmq_example/11_simulating_network_interruptions.py`  
- **README**: [README.md](rabbitmq_example/11_simulating_network_interruptions/README.md)  

### **12. Distributed Transactions**  
- **Description**: Implements **RabbitMQ transactions across multiple queues**.  
- **File**: `rabbitmq_example/12_distributed_transactions.py`  
- **README**: [README.md](rabbitmq_example/12_distributed_transactions/README.md)  

### **13. Testing with Mock Services**  
- **Description**: Mocks **external services interacting with RabbitMQ**.  
- **File**: `rabbitmq_example/13_testing_with_mock_services.py`  
- **README**: [README.md](rabbitmq_example/13_testing_with_mock_services/README.md)  

### **14. Security Testing**  
- **Description**: Tests RabbitMQ’s **authentication, authorization, and encryption mechanisms**.  
- **File**: `rabbitmq_example/14_security_testing.py`  
- **README**: [README.md](rabbitmq_example/14_security_testing/README.md)  

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
  docker ps | grep 5672  # RabbitMQ
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

## **🚀 Happy Testing with RabbitMQ and Testcontainers!** 🎉  

---
