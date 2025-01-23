print("🌟 Checking and Initializing MongoDB Replica Set...");

const cfg = {
    _id: "rs0",
    members: [{ _id: 0, host: "localhost:27017" }]
};

let rsInitiated = false;

while (!rsInitiated) {
    try {
        let status = rs.status();
        if (status.ok === 1) {
            print("✅ Replica set already initialized.");
            rsInitiated = true;
        } else {
            throw new Error("Replica set not initialized, proceeding...");
        }
    } catch (e) {
        print("⚠️ Replica set not initialized. Initializing now...");
        try {
            rs.initiate(cfg);
            rsInitiated = true;
            print("🎉 Replica set successfully initialized!");
        } catch (err) {
            print("⏳ Waiting for MongoDB to be ready before initializing again...");
            sleep(2000);
        }
    }
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

print("✅ MongoDB Replica Set is fully initialized and PRIMARY is elected!");
