print("🌟 Initializing MongoDB Replica Set...");

const cfg = {
    _id: "rs0",
    members: [{ _id: 0, host: "localhost:27017" }]
};

try {
    rs.initiate(cfg);
} catch (e) {
    print("⚠️ Replica set already initialized, skipping...");
}

let isReady = false;
while (!isReady) {
    try {
        let status = rs.status();
        if (status.ok === 1) {
            print("✅ MongoDB PRIMARY node is ready!");
            isReady = true;
        }
    } catch (e) {
        print("⏳ Waiting for PRIMARY node...");
        sleep(1000);
    }
}
