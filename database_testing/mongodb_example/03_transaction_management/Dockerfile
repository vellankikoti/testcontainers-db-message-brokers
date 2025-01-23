FROM mongo:6.0

# Copy the MongoDB initialization script
COPY mongo-init.js /docker-entrypoint-initdb.d/mongo-init.js

# ✅ Explicitly set MongoDB to start with replication
CMD ["mongod", "--replSet", "rs0", "--bind_ip_all"]
