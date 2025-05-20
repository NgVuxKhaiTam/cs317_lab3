#!/bin/bash
# filepath: /mlcv2/WorkingSpace/Personal/tuongbck/cs317/demo.sh

echo "=== RUL Prediction Service Demo ==="
echo "Building and starting Docker container..."
docker-compose up --build -d

echo -e "\nWaiting for the service to start (10 seconds)..."
sleep 10

echo -e "\n=== Testing the API ==="
echo "Sending a request to the API..."
curl -X POST "http://localhost:15000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_2": 445.0,
    "sensor_3": 549.68,
    "sensor_4": 1343.43,
    "sensor_7": 1112.93,
    "sensor_8": 3.91,
    "sensor_9": 5.7,
    "sensor_11": 137.36,
    "sensor_12": 2211.86,
    "sensor_13": 8311.32,
    "sensor_14": 1.01,
    "sensor_15": 41.69,
    "sensor_17": 129.78,
    "sensor_20": 2387.99,
    "sensor_21": 8074.83
  }'

echo -e "\n\n=== Demo completed ==="
echo "The Docker container is still running in the background."
echo "To stop it, use the command: docker-compose down"
