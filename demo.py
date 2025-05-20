#!/usr/bin/env python3
# filepath: /mlcv2/WorkingSpace/Personal/tuongbck/cs317/demo.py

import requests
import json
import time
import os
import subprocess
import sys

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
ENDC = "\033[0m"

def print_colored(text, color):
    print(f"{color}{text}{ENDC}")

def start_docker():
    print_colored("\n=== Starting Docker container ===", BLUE)
    result = subprocess.run(["docker-compose", "up", "--build", "-d"], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         text=True)
    if result.returncode != 0:
        print_colored("Error starting Docker container:", RED)
        print(result.stderr)
        sys.exit(1)
    else:
        print_colored("Docker container started successfully!", GREEN)

def test_api():
    print_colored("\n=== Waiting for API to be ready (10 seconds) ===", YELLOW)
    time.sleep(10)

    print_colored("\n=== Testing API ===", BLUE)
    api_url = "http://localhost:15000/predict"

    # Sample data for the API request
    sample_data = {
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
    }

    try:
        print_colored("Sending request to API...", YELLOW)
        response = requests.post(api_url, json=sample_data)
        
        if response.status_code == 200:
            print_colored("API request successful!", GREEN)
            
            # Pretty print the response
            response_data = response.json()
            print_colored("\nResponse:", BLUE)
            print(json.dumps(response_data, indent=2))
            
            # Extract the RUL prediction
            rul = response_data.get("Remaining Useful Life (RUL) prediction")
            if rul:
                print_colored(f"\nPredicted Remaining Useful Life: {rul}", GREEN)
        else:
            print_colored(f"API request failed with status code: {response.status_code}", RED)
            print(response.text)
    
    except Exception as e:
        print_colored(f"Error occurred: {str(e)}", RED)

def main():
    print_colored("=== RUL Prediction Service Demo ===", BLUE)
    
    # Ask if the user wants to start Docker
    start_docker_input = input("Do you want to start the Docker container? (y/n): ")
    if start_docker_input.lower() == 'y':
        start_docker()
        test_api()
    else:
        print_colored("Assuming Docker is already running...", YELLOW)
        test_api()
    
    print_colored("\n=== Demo completed ===", BLUE)
    print_colored("The Docker container is still running in the background.", YELLOW)
    print_colored("To stop it, use the command: docker-compose down", YELLOW)

if __name__ == "__main__":
    main()
