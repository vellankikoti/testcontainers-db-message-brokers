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

print("✅ Replica Set Initialized Successfully!");
