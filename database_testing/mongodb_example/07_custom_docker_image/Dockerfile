# Use the official MongoDB image
FROM mongo:6.0

# Copy initialization scripts
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Copy custom configuration
COPY mongod.conf /etc/mongod.conf

# Set environment variables
ENV MONGO_INITDB_DATABASE=bank_db

# Expose the default MongoDB port
EXPOSE 27017
