FROM mongo:6.0

# Copy MongoDB replica set initialization script
COPY mongo-init.js /docker-entrypoint-initdb.d/mongo-init.js

# ✅ Override the default entrypoint to force replica set
CMD ["mongod", "--replSet", "rs0", "--bind_ip_all"]
