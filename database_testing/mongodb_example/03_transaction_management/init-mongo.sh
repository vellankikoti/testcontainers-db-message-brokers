#!/bin/bash

echo "[INFO] ⏳ Waiting for MongoDB to start..."
until mongosh --host mongo-debug:27017 --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1; do
    sleep 2
done

echo "[INFO] ✅ MongoDB is up. Initializing Replica Set..."
mongosh --host mongo-debug:27017 <<EOF
rs.initiate({
  _id: "rs0",
  members: [{ _id: 0, host: "mongo-debug:27017" }]
});
EOF

# ✅ Wait until PRIMARY node is elected
echo "[INFO] ⏳ Waiting for MongoDB PRIMARY node election..."
until mongosh --host mongo-debug:27017 --eval "db.isMaster().ismaster" | grep "true"; do
    echo "[WARNING] 🚨 PRIMARY node not ready, retrying..."
    sleep 2
done

echo "[INFO] 🎉 PRIMARY Node Elected. MongoDB Ready!"
