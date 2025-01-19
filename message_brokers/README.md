# Message Brokers Testing with Testcontainers 🏨

Welcome to the Message Brokers Testing section! In this guide, we will explore how to use Testcontainers with three popular message brokers: **RabbitMQ**, **Kafka**, and **Redis**. Each message broker will be tested with practical examples that demonstrate how to perform various testing scenarios.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Message Brokers](#message-brokers)
    - [RabbitMQ](#rabbitmq)
    - [Kafka](#kafka)
    - [Redis](#redis)
- [Examples](#examples)
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
- [How to Run the Examples](#how-to-run-the-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

This repository contains a collection of examples demonstrating how to use Testcontainers with RabbitMQ, Kafka, and Redis for testing various message broker scenarios. Each example is designed to help you understand the concepts and implementation of message broker testing in a containerized environment.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Docker installed and running on your system
- Required Python packages for each message broker:
    ```bash
    pip install pytest pika kafka-python redis testcontainers
    ```

### Message Brokers

#### RabbitMQ
RabbitMQ is a widely used message broker that implements the Advanced Message Queuing Protocol (AMQP). In this section, you will find examples demonstrating how to interact with RabbitMQ using Testcontainers.

#### Kafka
Kafka is a distributed event streaming platform used for building real-time data pipelines and streaming applications. This section provides examples showcasing Kafka in a testing environment with Testcontainers.

#### Redis
Redis is an in-memory data structure store that can be used as a database, cache, or message broker. In this section, we provide examples for testing Redis with Testcontainers.

## Examples

### 01. Basic Guests
**Description:** Demonstrates a basic guest messaging system using the respective message broker and Testcontainers.  
**Files:**
- RabbitMQ: `rabbitmq_example/01_basic_guests.py`
- Kafka: `kafka_example/01_basic_guests.py`
- Redis: `redis_example/01_basic_guests.py`

### 02. Room Management
**Description:** Manages room availability and updates using the respective message broker.  
**Files:**
- RabbitMQ: `rabbitmq_example/02_room_management.py`
- Kafka: `kafka_example/02_room_management.py`
- Redis: `redis_example/02_room_management.py`

### 03. Reservations
**Description:** Implements a reservation system with messages being published and consumed from the message broker.  
**Files:**
- RabbitMQ: `rabbitmq_example/03_reservations.py`
- Kafka: `kafka_example/03_reservations.py`
- Redis: `redis_example/03_reservations.py`

### 04. Occupancy Report
**Description:** Generates room occupancy reports using a message-driven architecture.  
**Files:**
- RabbitMQ: `rabbitmq_example/04_occupancy_report.py`
- Kafka: `kafka_example/04_occupancy_report.py`
- Redis: `redis_example/04_occupancy_report.py`

### 05. Extended Stays
**Description:** Handles extended stays by sending and receiving messages related to stay duration updates.  
**Files:**
- RabbitMQ: `rabbitmq_example/05_extended_stays.py`
- Kafka: `kafka_example/05_extended_stays.py`
- Redis: `redis_example/05_extended_stays.py`

### 06. Simulating Failures
**Description:** Simulates message broker failures and handles message redelivery.  
**Files:**
- RabbitMQ: `rabbitmq_example/06_simulating_failures.py`
- Kafka: `kafka_example/06_simulating_failures.py`
- Redis: `redis_example/06_simulating_failures.py`

### 07. Custom Docker Image
**Description:** Builds and uses a custom Docker image with pre-configured messages and queues.  
**Files:**
- RabbitMQ: `rabbitmq_example/07_custom_docker_image.py`
- Kafka: `kafka_example/07_custom_docker_image.py`
- Redis: `redis_example/07_custom_docker_image.py`

### 08. Performance Testing
**Description:** Measures message broker performance under high-load scenarios.  
**Files:**
- RabbitMQ: `rabbitmq_example/08_performance_testing.py`
- Kafka: `kafka_example/08_performance_testing.py`
- Redis: `redis_example/08_performance_testing.py`

### 09. Data Migration Testing
**Description:** Validates data migration between different message brokers.  
**Files:**
- RabbitMQ: `rabbitmq_example/09_data_migration_testing.py`
- Kafka: `kafka_example/09_data_migration_testing.py`
- Redis: `redis_example/09_data_migration_testing.py`

### 10. Multiple Containers
**Description:** Verifies interactions between multiple containers (e.g., message brokers and databases).  
**Files:**
- RabbitMQ: `rabbitmq_example/10_multiple_containers.py`
- Kafka: `kafka_example/10_multiple_containers.py`
- Redis: `redis_example/10_multiple_containers.py`

### 11. Simulating Network Interruptions
**Description:** Tests message broker resilience during network disruptions.  
**Files:**
- RabbitMQ: `rabbitmq_example/11_simulating_network_interruptions.py`
- Kafka: `kafka_example/11_simulating_network_interruptions.py`
- Redis: `redis_example/11_simulating_network_interruptions.py`

### 12. Distributed Transactions
**Description:** Ensures message delivery across distributed systems with transactional integrity.  
**Files:**
- RabbitMQ: `rabbitmq_example/12_distributed_transactions.py`
- Kafka: `kafka_example/12_distributed_transactions.py`
- Redis: `redis_example/12_distributed_transactions.py`

### 13. Testing with Mock Services
**Description:** Simulates communication with a mocked payment service for integration testing.  
**Files:**
- RabbitMQ: `rabbitmq_example/13_testing_with_mock_services.py`
- Kafka: `kafka_example/13_testing_with_mock_services.py`
- Redis: `redis_example/13_testing_with_mock_services.py`

### 14. Security Testing
**Description:** Validates security configurations for message brokers.  
**Files:**
- RabbitMQ: `rabbitmq_example/14_security_testing.py`
- Kafka: `kafka_example/14_security_testing.py`
- Redis: `redis_example/14_security_testing.py`

## How to Run the Examples

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

3. Run an example:
    ```bash
    python <example-file>.py
    ```

    or

    ```bash
    python3 <example-file>.py
    ```

4. View the README file for detailed information about each example.

## Troubleshooting

### Common Issues

- **Docker Not Running:** Ensure Docker is installed and running on your system.
- **ModuleNotFoundError:** Install the required Python packages using:
    ```bash
    pip install pytest pika kafka-python redis testcontainers
    ```

- **Insufficient Resources:** Allocate more CPU and memory to Docker if containers fail to start.

## Contributing

Feel free to contribute by adding new examples, improving existing ones, or reporting issues.

Happy Testing! 🏨✨
