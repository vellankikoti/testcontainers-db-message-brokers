# Troubleshooting Guide for Testcontainers Setup

## Common Issues and Solutions

### 1. Docker Not Running
**Problem**: Docker is not running, and Testcontainers cannot start containers.

**Solution**:
- Ensure Docker Desktop is running (Windows/macOS).
- On Linux, start Docker with the following commands:
  ```bash
  sudo systemctl start docker
  ```
- Verify Docker is running by executing:
  ```bash
  docker info
  ```

---

### 2. Permission Issues with Docker
**Problem**: You encounter permission errors when running Docker commands.

**Solution**:
- On Linux, add your user to the Docker group:
  ```bash
  sudo usermod -aG docker $USER
  ```
- Log out and log back in for the changes to take effect.
- Verify by running:
  ```bash
  docker run hello-world
  ```

---

### 3. Python or Pip Not Found
**Problem**: Python or pip commands are not recognized.

**Solution**:
- Ensure Python is installed and added to your system PATH during installation.
- Verify Python installation:
  ```bash
  python --version
  ```
- If pip is not installed, install it manually:
  ```bash
  python -m ensurepip --upgrade
  ```

---

### 4. Testcontainers Import Error
**Problem**: You encounter an error when importing the Testcontainers library.

**Solution**:
- Ensure the `testcontainers` library is installed:
  ```bash
  pip install testcontainers
  ```
- Verify the installation by running:
  ```bash
  python -c "import testcontainers; print('Testcontainers installed successfully!')"
  ```

---

### 5. Container Fails to Start
**Problem**: The container does not start or exits immediately.

**Solution**:
- Check the container logs for errors:
  ```python
  logs = container.get_logs()
  print(logs)
  ```
- Ensure the Docker image exists and is compatible with your system.
- Pull the latest version of the image manually:
  ```bash
  docker pull <image_name>
  ```

---

### 6. Port Mapping Issues
**Problem**: Unable to access the service running inside the container.

**Solution**:
- Ensure the port is exposed in the container:
  ```python
  container.with_exposed_ports(<port_number>)
  ```
- Retrieve the mapped host port:
  ```python
  host_port = container.get_exposed_port(<port_number>)
  ```
- Verify the service is running by accessing `http://localhost:<host_port>`.

---

### 7. Docker Image Not Found
**Problem**: Docker cannot find the specified image.

**Solution**:
- Verify the image name and tag are correct.
- Pull the image manually:
  ```bash
  docker pull <image_name>:<tag>
  ```

---

### 8. Outdated Docker or Testcontainers Version
**Problem**: Compatibility issues due to outdated versions.

**Solution**:
- Update Docker to the latest version:
  ```bash
  sudo apt update && sudo apt upgrade docker.io
  ```
- Update the Testcontainers library:
  ```bash
  pip install --upgrade testcontainers
  ```

---

### 9. Network Connectivity Issues
**Problem**: Containers cannot access the internet or communicate with each other.

**Solution**:
- Ensure your Docker network is configured correctly.
- Restart Docker to reset the network:
  ```bash
  sudo systemctl restart docker
  ```

---

### 10. Debugging Tips
- Use the `docker ps` command to list running containers.
- Use the `docker logs <container_id>` command to view container logs.
- Use the `docker inspect <container_id>` command to inspect container details.

---

## Need More Help?
If you encounter issues not covered in this guide, consider:
- Checking the [Testcontainers documentation](https://testcontainers.com/).
- Searching for solutions on forums like Stack Overflow.
- Reviewing Docker's official troubleshooting guide.

---

This guide should help you resolve most common issues when setting up and using Testcontainers. Happy testing!