const startTime = new Date();
const timeout = 60000; // 60 seconds

while (true) {
    try {
        let status = rs.status();
        if (status.myState === 1) {
            print("✅ Replica Set is PRIMARY. Initialization complete.");
            break;
        }
    } catch (err) {
        print("⏳ Waiting for PRIMARY election...");
    }

    if (new Date() - startTime > timeout) {
        print("❌ Timeout waiting for PRIMARY node!");
        quit(1);
    }
    sleep(2000);
}

// Initialize the replica set if not already initialized
try {
    let cfg = {
        _id: "rs0",
        members: [
            { _id: 0, host: "mongo-db:27017" }
        ]
    };
    rs.initiate(cfg);
    print("✅ Replica Set Initialized!");
} catch (err) {
    print("⚠️ Replica Set already initialized.");
}

print("✅ MongoDB Ready for Transactions!");
