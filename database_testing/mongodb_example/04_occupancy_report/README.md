# Example 4: Occupancy Report (MongoDB)

This example demonstrates how to use Testcontainers to generate and test hotel occupancy reports using MongoDB. It covers:

- Calculating occupancy rates.
- Generating revenue reports.
- Analyzing room type distribution.
- Creating historical occupancy trends.

---

## Overview

The test simulates a hotel reporting system that:

1. Calculates daily/monthly occupancy rates.
2. Generates revenue reports by room type.
3. Analyzes booking patterns.
4. Tracks historical occupancy data.
5. Creates forecasting metrics.

---

## Features

### Occupancy Calculations

- Daily occupancy rates.
- Monthly occupancy trends.
- Room type distribution.
- Peak period analysis.

### Revenue Analysis

- Revenue by room type.
- Average daily rate (ADR).
- Revenue per available room (RevPAR).
- Historical revenue trends.

### Report Generation

- Custom date ranges.
- Room type filtering.
- Status-based reporting.
- Trend analysis.

---

## How to Run the Test

### 1. Install Dependencies

Install the required Python packages using `pip` or `pip3`:

```bash
pip install pytest testcontainers pymongo pandas
```

or

```bash
pip3 install pytest testcontainers pymongo pandas
```

### 2. Run the Test

Execute the test file using `pytest`:

```bash
python -m pytest 04_occupancy_report.py -v -s
```

or

```bash
python3 -m pytest 04_occupancy_report.py -v -s
```

---

## Expected Output

When you run the test, you should see output similar to the following:

![image](https://github.com/user-attachments/assets/64233de4-7a73-4c31-afb1-cba690252cba)


## Code Walkthrough

### 1. Report Schema

```python
occupancy_report = {
    "date": "2024-01-01",
    "total_rooms": 100,
    "occupied_rooms": 75,
    "occupancy_rate": 75.0,
    "revenue": 15000.00,
    "adr": 200.00,
    "revpar": 150.00,
    "room_type_distribution": {
        "standard": 40,
        "deluxe": 25,
        "suite": 10
    }
}
```

### 2. Key Operations

- Calculate occupancy metrics.
- Generate revenue reports.
- Analyze room distribution.
- Create historical trends.
- Generate forecasts.

### 3. Test Cases

- Daily occupancy calculations.
- Revenue report generation.
- Room type distribution analysis.
- Historical trend analysis.
- Occupancy forecasting.

---

## Key Takeaways

### MongoDB Benefits

- Flexible report schema.
- Efficient aggregation.
- Easy date handling.
- Complex queries.

### Testing Practices

- Comprehensive metrics.
- Data validation.
- Clear organization.
- Proper cleanup.

### Reporting System

- Accurate calculations.
- Multiple metrics.
- Trend analysis.
- Forecasting capabilities.

---

## Common Issues and Solutions

### 1. Data Aggregation

- Use proper indexing.
- Optimize queries.
- Handle large datasets.

### 2. Date Handling

- Standardize timezone.
- Handle date ranges.
- Manage historical data.

### 3. Performance

- Implement caching.
- Use efficient queries.
- Handle concurrent reports.

---

## Future Enhancements

### Planned Features

- Real-time reporting.
- Advanced forecasting.
- Custom metrics.
- Interactive dashboards.

### Testing Improvements

- Performance testing.
- Large dataset handling.
- Extended date ranges.
- Complex aggregations.

---
