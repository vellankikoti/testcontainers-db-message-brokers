# **Core Concepts of Testcontainers**

## **Objective**
To understand the foundational concepts of Testcontainers, including the lifecycle of containers, how to start and stop them, and how to access logs and ports, with real-world examples and visual aids.

---

## **What is a Container?**
- A **container** is a lightweight, standalone, and executable package that includes everything needed to run a piece of software: the code, runtime, libraries, and system tools.
- Containers are isolated from each other and the host system, ensuring consistent behavior across different environments.
- **Docker** is the most popular tool for creating and managing containers.

### **Real-World Example**
Imagine you are developing a web application that uses a **PostgreSQL database**. Instead of installing PostgreSQL on your local machine, you can run it in a container. This ensures:
1. The database runs in isolation, avoiding conflicts with other software.
2. You can easily reset the database by restarting the container.

---

## **What is Testcontainers?**
- **Testcontainers** is a library that simplifies the use of Docker containers for testing purposes.
- It allows you to:
  - Spin up lightweight, disposable containers for testing.
  - Run databases, message brokers, or any other services in containers during tests.
  - Automatically manage the lifecycle of containers (start, stop, and cleanup).

### **Real-World Example**
You are writing integration tests for your application, which interacts with a **Redis cache**. Using Testcontainers, you can:
1. Start a Redis container before the test.
2. Run your test against the Redis instance.
3. Automatically stop and clean up the container after the test.

---

## **Lifecycle of a Testcontainer**
The lifecycle of a Testcontainer involves the following steps:

| **Step**       | **Description**                                                                 |
|-----------------|---------------------------------------------------------------------------------|
| **Creation**    | A Testcontainer is created using a specific Docker image.                      |
| **Starting**    | The container is started, and any necessary setup (like environment variables or port mappings) is applied. |
| **Running**     | The container runs until it is stopped or removed.                             |
| **Stopping**    | The container can be stopped manually or automatically when the test completes. |
| **Removal**     | The container is removed from the Docker host to free up resources.            |

### **Diagram: Testcontainer Lifecycle**
```plaintext
+----------------+       +----------------+       +----------------+       +----------------+
|   Creation     | ----> |    Starting    | ----> |    Running     | ----> |    Stopping    |
+----------------+       +----------------+       +----------------+       +----------------+
                                                             |
                                                             v
                                                    +----------------+
                                                    |    Removal     |
                                                    +----------------+
```

---

## **Step-by-Step Instructions**

### **Step 1: Creating and Starting a Testcontainer**
1. Create a new Python file called `test_container_lifecycle.py`:
```python
from testcontainers.core.container import DockerContainer
import time

def test_simple_container():
    print("\n=== Simple Container Test ===")

    with DockerContainer("alpine:latest") as container:
        # Get container ID
        container_id = container._container.id
        print(f"Container ID: {container_id}")

        # Get container status
        status = container._container.status
        print(f"Container Status: {status}")

        # Wait a moment
        time.sleep(2)
        print("Container is running...")

if __name__ == "__main__":
    test_simple_container()
```
   **Explanation:**
   - `DockerContainer("alpine:latest")`: Creates a container using the lightweight Alpine Linux image.
   - `with ... as container`: Automatically starts the container and ensures it is stopped and cleaned up after use.
   - `container._container.id`: Retrieves the unique ID of the running container.

2. Run the script:
   ```bash
   python test_container_lifecycle.py
   ```

   **Output Example:**

![image](https://github.com/user-attachments/assets/1202a33d-0f7c-41fd-b710-01cebbc7ecd0)


---

### **Step 2: Accessing Container Logs**
1. Modify the script to access logs:
```python
from testcontainers.core.container import DockerContainer
import time

def test_container_with_logs():
    print("\n=== Container Test with Logs ===")

    # Use a script that generates some interesting logs
    startup_command = """
    while true; do
        echo "Hello from Alpine container!"
        echo "Current time: $(date)"
        echo "Container is alive and well..."
        sleep 2
    done
    """

    with DockerContainer("alpine:latest").with_command(["/bin/sh", "-c", startup_command]) as container:
        # Get container ID
        container_id = container._container.id
        print(f"Container ID: {container_id}")

        # Wait for logs to generate
        time.sleep(5)

        # Get container status
        container._container.reload()
        status = container._container.status
        print(f"Container Status: {status}")

        # Get container logs
        print("\nContainer Logs:")
        logs = container._container.logs()
        print(logs.decode('utf-8'))

if __name__ == "__main__":
    test_container_with_logs()

```
   **Explanation:**
   - `container._container.logs()`: Retrieves the logs generated by the container.

2. Run the script:
   ```bash
   python test_container_lifecycle.py
   ```

   **Output Example:**

![image](https://github.com/user-attachments/assets/e7a1dc54-f98d-424b-a846-3898a2a17d24)


---

### **Step 3: Mapping Ports**
1. Modify the script to map a port from the container to the host:
```python
from testcontainers.core.container import DockerContainer
import time
import requests

def test_port_mapping():
    print("\n=== Port Mapping Test ===")

    # Using nginx as it provides a web server we can test
    with DockerContainer("nginx:latest").with_exposed_ports(80) as container:
        # Get container ID
        container_id = container._container.id
        print(f"Container ID: {container_id}")

        # Get the mapped port
        mapped_port = container.get_exposed_port(80)
        print(f"Nginx is running on port: {mapped_port}")

        # Wait for nginx to start
        time.sleep(2)

        # Try to access nginx
        try:
            response = requests.get(f"http://localhost:{mapped_port}")
            print(f"\nNginx Response Status Code: {response.status_code}")
            print("Successfully connected to Nginx!")
        except Exception as e:
            print(f"Error connecting to Nginx: {e}")

if __name__ == "__main__":
    test_port_mapping()
```
   **Explanation:**
   - `container.with_exposed_ports(80)`: Exposes port 80 (default HTTP port) from the container.
   - `container.get_exposed_port(80)`: Retrieves the port on the host machine that maps to port 80 in the container.

2. Run the script:
   ```bash
   python test_container_lifecycle.py
   ```

   **Output Example:**
![image](https://github.com/user-attachments/assets/f812e4ca-4926-4323-a6db-ece8277ba297)


3. Open a browser and navigate to `http://localhost:<host_port>` (e.g., `http://localhost:49153`). You should see the default NGINX welcome page.
![image](https://github.com/user-attachments/assets/d5ffcaa9-31e4-4415-b1c8-571d21b34689)

---

## **Real-World Use Cases**

| **Use Case**           | **Description**                                              |
|-------------------------|-------------------------------------------------------------|
| **Database Testing**    | Spin up a PostgreSQL or MySQL container for integration tests. |
| **Message Broker Testing** | Test your application with RabbitMQ or Kafka containers.   |
| **Web Server Testing**  | Run an NGINX or Apache container to test web server configurations. |
| **Custom Docker Images**| Use your own Docker images to test specific application setups. |

---

## **Key Takeaways**
- Learned the basics of Testcontainers, including creating, starting, and stopping containers.
- Accessed container logs and mapped ports to interact with services running inside containers.
- Testcontainers automatically manages the lifecycle of containers, ensuring a clean environment for each test.

---
