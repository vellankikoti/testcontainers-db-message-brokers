# **Message Brokers Testing with Testcontainers 🏨**

Welcome to the **Message Brokers Testing** section! This guide provides a **comprehensive overview** of how to use **Testcontainers** with **three popular message brokers**: **RabbitMQ, Kafka, and Redis**. Each broker is tested with **real-world examples** that validate **message integrity, persistence, resilience, and performance**.

---

## **Table of Contents**

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Message Brokers](#message-brokers)
  - [RabbitMQ](#rabbitmq)
  - [Kafka](#kafka)
  - [Redis](#redis)
- [Examples](#examples)
  - [01. Basic Publish/Subscribe Operations](#01-basic-publish-subscribe-operations)
  - [02. Message Persistence](#02-message-persistence)
  - [03. Data Integrity Testing](#03-data-integrity-testing)
  - [04. Performance Testing](#04-performance-testing)
  - [05. Field Constraints & Index Testing](#05-field-constraints--index-testing)
  - [06. Simulating Failures](#06-simulating-failures)
  - [07. Custom Docker Image](#07-custom-docker-image)
  - [08. Load Testing](#08-load-testing)
  - [09. Data Migration Testing](#09-data-migration-testing)
  - [10. Multiple Containers](#10-multiple-containers)
  - [11. Simulating Network Interruptions](#11-simulating-network-interruptions)
  - [12. Distributed Transactions](#12-distributed-transactions)
  - [13. Testing with Mock Services](#13-testing-with-mock-services)
  - [14. Security Testing](#14-security-testing)
- [How to Run the Examples](#how-to-run-the-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## **Overview**

This repository provides **real-world examples** demonstrating **how to use Testcontainers** with **RabbitMQ, Kafka, and Redis** for **message broker testing** in Python. Each section **follows a structured approach**, starting from **basic publish/subscribe operations** to **advanced resilience, performance, and security testing**.

---

## **Getting Started**

### **Prerequisites**

- **Python 3.10** or later
- **Docker installed and running** on your system
- Required Python packages for each message broker:
  ```bash
  pip install pytest pika kafka-python redis testcontainers
  ```

---

## **Message Brokers**

### **RabbitMQ**
RabbitMQ is a widely used **message broker** that implements the **Advanced Message Queuing Protocol (AMQP)**. This section demonstrates **how to use Testcontainers for RabbitMQ testing**.

### **Kafka**
Kafka is a **distributed event streaming platform** used for building **real-time data pipelines and streaming applications**. This section provides **Kafka testing examples** using **Testcontainers**.

### **Redis**
Redis is an **in-memory data structure store** that can be used as a **database, cache, or message broker**. This section includes examples of **using Testcontainers to test Redis messaging features**.

---

## **Examples**

### **01. Basic Publish/Subscribe Operations**
- **Description**: Tests the basic ability to **send and receive messages** via the respective message broker.
- **Files**:
  - RabbitMQ: `rabbitmq_example/01_basic_pub_sub.py`
  - Kafka: `kafka_example/01_basic_pub_sub.py`
  - Redis: `redis_example/01_basic_pub_sub.py`

### **02. Message Persistence**
- **Description**: Verifies that **messages persist** across broker restarts (where applicable).
- **Files**:
  - RabbitMQ: `rabbitmq_example/02_message_persistence.py`
  - Kafka: `kafka_example/02_message_persistence.py`
  - Redis: `redis_example/02_message_persistence.py`

### **03. Data Integrity Testing** (Updated ✅)
- **Description**: Ensures **message integrity** by testing:
  - **RabbitMQ**: Validates **message ordering, delivery guarantees, and duplicate prevention**.
  - **Kafka**: Ensures **message durability, correct partitioning, and exactly-once semantics**.
  - **Redis**: Tests **message consistency in streams and pub/sub models**.
- **Files**:
  - RabbitMQ: `rabbitmq_example/03_data_integrity_testing.py`
  - Kafka: `kafka_example/03_data_integrity_testing.py`
  - Redis: `redis_example/03_data_integrity_testing.py`

### **04. Performance Testing**
- **Description**: Measures the **message broker’s performance under high-load scenarios**.
- **Files**:
  - RabbitMQ: `rabbitmq_example/04_performance_testing.py`
  - Kafka: `kafka_example/04_performance_testing.py`
  - Redis: `redis_example/04_performance_testing.py`

### **05. Field Constraints & Index Testing** (Updated ✅)
- **Description**: Ensures the **message broker handles constraints correctly** and **optimizes queries with indexing**.
  - **RabbitMQ**: Tests **queue durability, message TTL, and dead-letter exchanges**.
  - **Kafka**: Ensures **topic configurations, partition indexing, and message retention policies**.
  - **Redis**: Validates **message expirations, data type constraints, and indexing**.
- **Files**:
  - RabbitMQ: `rabbitmq_example/05_field_constraints_and_indexes.py`
  - Kafka: `kafka_example/05_field_constraints_and_indexes.py`
  - Redis: `redis_example/05_field_constraints_and_indexes.py`

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
  docker ps | grep 9092  # Kafka
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

## **🚀 Happy Testing!**

---
