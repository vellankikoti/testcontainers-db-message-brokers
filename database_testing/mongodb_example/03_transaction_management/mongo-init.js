// mongo-init.js
print("🚀 Initiating MongoDB replica set...");
rs.initiate({
    _id: "rs0",
    members: [{ _id: 0, host: "mongo-debug:27017" }]
});
print("🎉 Replica set initialized successfully!");
