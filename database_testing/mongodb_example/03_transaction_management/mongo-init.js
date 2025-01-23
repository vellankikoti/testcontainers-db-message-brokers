print("🌟 Checking and Initializing MongoDB Replica Set...");

const cfg = {
    _id: "rs0",
    members: [{ _id: 0, host: "localhost:27017" }]
};

try {
    let status = rs.status();
    if (status.ok === 1) {
        print("✅ Replica set already initialized.");
    } else {
        throw new Error("Replica set not initialized, proceeding...");
    }
} catch (e) {
    print("⚠️ Initializing replica set...");
    rs.initiate(cfg);
}

// ✅ Wait until MongoDB elects a PRIMARY node
print("⏳ Waiting for MongoDB PRIMARY node election...");
let isReady = false;
while (!isReady) {
    try {
        let status = rs.status();
        if (status.ok === 1 && status.myState === 1) {
            print("🎉 MongoDB PRIMARY node is ready!");
            isReady = true;
        }
    } catch (e) {
        print("⏳ Still waiting for PRIMARY node...");
        sleep(2000);
    }
}
