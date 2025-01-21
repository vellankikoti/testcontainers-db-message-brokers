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
    - [01. Basic Publish/Subscribe Operations](#01-basic-publish-subscribe-operations)
    - [02. Message Persistence](#02-message-persistence)
    - [03. Message Acknowledgements](#03-message-acknowledgements)
    - [04. Performance Testing](#04-performance-testing)
    - [05. Resilience Testing](#05-resilience-testing)
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
RabbitMQ is a widely used message broker that implements the Advanced Message Queuing Protocol (AMQP). This section demonstrates how to use Testcontainers for RabbitMQ testing.

#### Kafka
Kafka is a distributed event streaming platform used for building real-time data pipelines and streaming applications. This section provides examples showcasing Kafka in a testing environment with Testcontainers.

#### Redis
Redis is an in-memory data structure store that can be used as a database, cache, or message broker. This section includes examples of using Testcontainers to test Redis messaging features.

## Examples

### 01. Basic Publish/Subscribe Operations
**Description:** Tests the basic ability to send and receive messages via the respective message broker.
**Files:**
- RabbitMQ: `rabbitmq_example/01_basic_pub_sub.py`
- Kafka: `kafka_example/01_basic_pub_sub.py`
- Redis: `redis_example/01_basic_pub_sub.py`

### 02. Message Persistence
**Description:** Verifies that messages persist across broker restarts where applicable.
**Files:**
- RabbitMQ: `rabbitmq_example/02_message_persistence.py`
- Kafka: `kafka_example/02_message_persistence.py`
- Redis: `redis_example/02_message_persistence.py`

### 03. Message Acknowledgements
**Description:** Ensures that messages are acknowledged and re-queued appropriately.
**Files:**
- RabbitMQ: `rabbitmq_example/03_message_acknowledgements.py`
- Kafka: `kafka_example/03_message_acknowledgements.py`
- Redis: `redis_example/03_message_acknowledgements.py`

### 04. Performance Testing
**Description:** Measures the message broker’s performance under high-load scenarios.
**Files:**
- RabbitMQ: `rabbitmq_example/04_performance_testing.py`
- Kafka: `kafka_example/04_performance_testing.py`
- Redis: `redis_example/04_performance_testing.py`

### 05. Resilience Testing
**Description:** Tests the ability of message brokers to recover from failures.
**Files:**
- RabbitMQ: `rabbitmq_example/05_resilience_testing.py`
- Kafka: `kafka_example/05_resilience_testing.py`
- Redis: `redis_example/05_resilience_testing.py`

### 06. Simulating Failures
**Description:** Simulates message broker failures and handles message redelivery.
**Files:**
- RabbitMQ: `rabbitmq_example/06_simulating_failures.py`
- Kafka: `kafka_example/06_simulating_failures.py`
- Redis: `redis_example/06_simulating_failures.py`

### 07. Custom Docker Image
**Description:** Builds and uses a custom Docker image with pre-configured queues and topics.
**Files:**
- RabbitMQ: `rabbitmq_example/07_custom_docker_image.py`
- Kafka: `kafka_example/07_custom_docker_image.py`
- Redis: `redis_example/07_custom_docker_image.py`

### 08. Load Testing
**Description:** Simulates message loads to evaluate broker performance.
**Files:**
- RabbitMQ: `rabbitmq_example/08_load_testing.py`
- Kafka: `kafka_example/08_load_testing.py`
- Redis: `redis_example/08_load_testing.py`

### 09. Data Migration Testing
**Description:** Ensures messages are successfully migrated between different brokers.
**Files:**
- RabbitMQ: `rabbitmq_example/09_data_migration_testing.py`
- Kafka: `kafka_example/09_data_migration_testing.py`
- Redis: `redis_example/09_data_migration_testing.py`

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

3. Run an example:
    ```bash
    python <example-file>.py
    ```

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

