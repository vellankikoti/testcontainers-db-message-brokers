rs.initiate(
  {
    _id: "rs0",
    version: 1,
    members: [
      { _id: 0, host: "mongo:27017" }
    ]
  }
);

while (!rs.isMaster().ismaster) {
  sleep(100);
}

print("✅ Replica Set Initialized Successfully!");
