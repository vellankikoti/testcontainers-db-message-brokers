# Example 7: Custom Docker Image (MongoDB)

This example demonstrates how to create and test a custom MongoDB Docker image with Testcontainers. It covers:

- Building custom MongoDB Docker images.
- Pre-loading test data.
- Custom MongoDB configurations.
- Testing with custom images.

---

## Overview

The test uses a custom MongoDB Docker image that includes:

- **Pre-loaded test data**
- **Custom MongoDB configuration**
- **Initialization scripts**
- **Custom user credentials**

---

## Features

### Custom Docker Image

- Base MongoDB image customization.
- Data pre-loading capabilities.
- Custom configuration settings.
- Initialization scripts.

### Pre-loaded Data

- Sample hotel data.
- Test user accounts.
- Configuration settings.
- Initial collections.

### Custom Configuration

- MongoDB settings.
- Authentication setup.
- Network configuration.
- Storage options.

---

## How to Run the Test

### 1. Build Custom Docker Image

Build the custom Docker image using the provided Dockerfile:

```bash
docker build -t custom-mongodb:1.0 .
```

### 2. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo
```

or

```bash
pip3 install pytest testcontainers pymongo
```

### 3. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 07_custom_docker_image.py -v -s
```

or

```bash
python3 -m pytest 07_custom_docker_image.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/7ba7457b-8b1a-4fa4-8cc2-f1049794ce28)



---

## Key Takeaways

### Docker Benefits

- **Reproducible environments**.
- **Pre-loaded test data**.
- **Custom configurations**.
- **Portable setup**.

### Testing Practices

- Isolated test environment.
- Consistent test data.
- Configuration validation.
- Clean test execution.

### Custom Image Benefits

- Faster test execution.
- Consistent test data.
- Reproducible tests.
- Simplified setup.

---

## Common Issues and Solutions

### 1. Image Building

- Verify Dockerfile syntax.
- Check file permissions.
- Validate initialization scripts.
- Test configuration files.

### 2. Container Startup

- Check port availability.
- Verify environment variables.
- Monitor initialization logs.
- Validate data loading.

### 3. Test Execution

- Ensure image availability.
- Check container logs.
- Verify data loading.
- Test connectivity.

---

## Future Enhancements

### Planned Features

- Multi-stage builds.
- Advanced data seeding.
- Dynamic configurations.
- Health checks.

### Testing Improvements

- Performance benchmarks.
- Configuration testing.
- Data validation.
- Startup optimization.

---
