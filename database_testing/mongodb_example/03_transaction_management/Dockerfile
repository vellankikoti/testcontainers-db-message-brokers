FROM mongo:6.0

# Copy the MongoDB initialization script
COPY mongo-init.js /docker-entrypoint-initdb.d/mongo-init.js

# ✅ Set MongoDB to run as a replica set
CMD ["mongod", "--replSet", "rs0", "--bind_ip_all"]
