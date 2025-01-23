FROM mongo:6.0

# Copy the MongoDB initialization script
COPY mongo-init.js /docker-entrypoint-initdb.d/mongo-init.js

# ✅ Override the default entrypoint to force `--replSet rs0`
ENTRYPOINT ["mongod", "--replSet", "rs0", "--bind_ip_all"]
