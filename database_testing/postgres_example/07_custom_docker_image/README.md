# Example 7: Custom Docker Image

## Overview
This example demonstrates how to use a custom Docker image for testing database-related functionality. Instead of relying on a standard PostgreSQL image, we create and use a custom image with preloaded data or specific configurations to meet advanced testing requirements.

---

## Key Concepts

### Custom Docker Image
- Preloaded database schema and data.
- Custom configurations (e.g., extensions, environment variables).
- Tailored for specific testing scenarios.

### Testing Approach
- Build and use a custom Docker image.
- Verify the preloaded data and configurations.
- Run tests against the custom image.

---

## Code Structure

### Main Components

#### Custom Docker Image
A `Dockerfile` is used to create a custom PostgreSQL image with preloaded data and configurations.

#### Database Setup
The database schema and data are preloaded into the custom image during the build process.

#### Test Cases
- Verify the custom image is loaded correctly.
- Validate the preloaded data and configurations.

---

## Running the Tests

### 1. Prerequisites
- **Python 3.8+**
- **Docker** installed and running.
- Required packages:
  ```bash
  pip install pytest testcontainers sqlalchemy psycopg2-binary
  ```

### 2. Build the Custom Docker Image
Navigate to the directory containing the `Dockerfile` and run:
```bash
docker build -t custom-postgres:1.0 .
```

### 3. Execution
Build the Docker image first
```bash
docker build -t custom-postgres:1.0 .
```
Run the test file using pytest:
```bash
python -m pytest 07_custom_docker_image.py -v
```
or
```bash
python3 -m pytest 07_custom_docker_image.py -v
```
---

## Expected Output
![image](https://github.com/user-attachments/assets/429a9b4d-2e17-4e7c-8d1f-0d9f37accefd)


---

## Key Takeaways

### Custom Docker Images
- Useful for advanced testing scenarios.
- Preload schema, data, and configurations.
- Tailor the environment to specific needs.

### Testing with Custom Images
- Validate the image is built and loaded correctly.
- Verify preloaded data and configurations.
- Ensure compatibility with the application.

### Advantages
- Faster test setup (preloaded data).
- Consistent testing environment.
- Customizable for specific use cases.

---

## Common Pitfalls

### Docker Image Issues
- Incorrect Dockerfile syntax.
- Missing dependencies in the image.
- Incorrect database configurations.

### Test Failures
- Preloaded data not matching expectations.
- Connection issues with the custom image.
- Misconfigured environment variables.

---

## Debugging Tips

### Common Issues
- Docker image build failures.
- Connection errors.
- Missing or incorrect preloaded data.

### Solutions
- Check the Dockerfile for syntax errors.
- Verify the image build logs.
- Test the custom image manually using `docker run`.

---

## Future Enhancements

### Additional Test Scenarios
- Use custom images for other databases (e.g., MySQL, MongoDB).
- Test with multiple custom images.
- Automate the image build process.

### Improvements
- Add more preloaded data.
- Include database extensions in the custom image.
- Optimize the image size and build time.

---

## Related Documentation
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [pytest Documentation](https://docs.pytest.org/en/latest/)
- [TestContainers Python](https://testcontainers-python.readthedocs.io/)

---
