db.createCollection('banks');
db.hotels.insertMany([
    {
        "name": "State Bank",
        "branches": 100,
        "location": "Downtown"
    },
    {
        "name": "Koti Inn",
        "rooms": 50,
        "location": "Uptown"
    }
    // Add more pre-loaded data as needed...
]);
