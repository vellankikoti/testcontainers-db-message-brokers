# Setup Section

## 1. Setting Up the Environment

### Objective
To set up the required tools and environment to start using Testcontainers with Python.

---

### Prerequisites
Before we begin, ensure you have the following:
- A computer with Windows, macOS, or Linux.
- Python 3.10 or later installed (we are using Python 3.10.12 for this guide).
- Docker installed and running.

---

## Step-by-Step Instructions

### Step 1: Install Python

#### Check if Python is already installed:
Open a terminal or command prompt and type:
```bash
python --version
```
or
```bash
python3 --version
```
If Python is installed, you’ll see the version number. Ensure it’s **3.10 or later**.

#### Install Python (if not installed):
**Windows**:
- Download the latest Python 3.10+ installer from the [official Python website](https://www.python.org/).
- Run the installer and check the box **"Add Python to PATH"** during installation.

**macOS**:
- Use Homebrew (if installed):
  ```bash
  brew install python@3.10
  ```
- Or download the installer from the [official Python website](https://www.python.org/).

**Linux**:
- Use your package manager:
  ```bash
  sudo apt update
  sudo apt install python3.10 python3.10-venv python3.10-dev
  ```

#### Verify Python installation:
Run:
```bash
python --version
```
or
```bash
python3 --version
```
You should see something like:

![image](https://github.com/user-attachments/assets/56e0f4f1-8562-44e4-84a6-e0bfadb4587a)


**Note**: We are using Python 3.10.12 for this guide, but you can use any version of Python 3.10 or later.

---

### Step 2: Install Docker

#### Check if Docker is already installed:
Open a terminal or command prompt and type:
```bash
docker --version
```
If Docker is installed, you’ll see the version number.

#### Install Docker (if not installed):
**Windows**:
- Download Docker Desktop from the [official Docker website](https://www.docker.com/).
- Run the installer and follow the instructions.
- After installation, start Docker Desktop and ensure it’s running.

**macOS**:
- Download Docker Desktop from the [official Docker website](https://www.docker.com/).
- Install and start Docker Desktop.

**Linux**:
- Use your package manager:
  ```bash
  sudo apt update
  sudo apt install docker.io
  ```
- Start Docker:
  ```bash
  sudo systemctl start docker
  sudo systemctl enable docker
  ```

#### Verify Docker installation:
Run:
```bash
docker --version
```
You should see something like:

![image](https://github.com/user-attachments/assets/e3bc1d00-dcfa-45cf-890d-ef2243aa8745)


#### Test Docker installation:
Run:
```bash
docker run hello-world
```
This will pull a test image and run it. If everything is set up correctly, you’ll see a message like:
```
Hello from Docker!
```

---

### Step 3: Install Testcontainers for Python

#### Install the `testcontainers` library:
Run:
```bash
pip install testcontainers
```
or, if you’re using Python 3:
```bash
pip3 install testcontainers
```

#### Verify installation:
Run:
```bash
python3 -c 'import testcontainers; print("Testcontainers installed successfully!")'
```
If there are no errors, the installation was successful.

![image](https://github.com/user-attachments/assets/41fd76b1-28ef-469a-89c2-69c4c41b2251)

---

### Step 4: Verify the Setup

1. Create a new Python file called `test_setup.py`:
   ```python
from testcontainers.core.container import DockerContainer

# Create and start a container
with DockerContainer("alpine:latest") as container:
    print(f"Container started with ID: {container._container.id}")
    # Or you can use container.get_container_id() method if available
   ```

2. Run the script:
   ```bash
   python test_setup.py
   ```

If everything is set up correctly, you’ll see output like:

![image](https://github.com/user-attachments/assets/6b652d0e-bbd9-4537-8000-cda99246b432)

---

## Troubleshooting

### Docker not running:
- Ensure Docker Desktop is running (Windows/macOS).
- On Linux, start Docker with:
  ```bash
  sudo systemctl start docker
  ```

### Permission issues with Docker:
- On Linux, add your user to the Docker group:
  ```bash
  sudo usermod -aG docker $USER
  ```
- Then log out and log back in.

### Python or pip not found:
- Ensure Python is added to your system PATH during installation.

### Testcontainers import error:
- Ensure the `testcontainers` library is installed:
  ```bash
  pip install testcontainers
  ```

---

## Versions Used
- **Python**: 3.10.12 (recommended: 3.10+)
- **Docker**: 24.0.
- **Testcontainers**: 6.0.0

---

## Key Takeaways
- You’ve successfully set up Python 3.10+ (we used 3.10.12), Docker, and Testcontainers.
- You’ve verified the setup by running a simple container.
- You’re ready to dive into Testcontainers and start testing!

---
