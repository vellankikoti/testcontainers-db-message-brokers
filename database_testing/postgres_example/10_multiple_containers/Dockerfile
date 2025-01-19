# Use PostgreSQL 15.3 as the base image
FROM postgres:15.3

# Set environment variables
ENV POSTGRES_DB=testdb
ENV POSTGRES_USER=testuser
ENV POSTGRES_PASSWORD=testpass

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Install additional PostgreSQL extensions if needed
RUN apt-get update && apt-get install -y \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*
