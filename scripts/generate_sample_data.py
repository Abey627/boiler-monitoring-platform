#!/usr/bin/env python
"""
Sample data generator for the Boiler Monitoring Platform
This script creates sample boiler sites, sensors, and generates mock IoT data
"""

import os
import sys
import json
import random
import requests
from datetime import datetime, timedelta

# Sample boiler sites data
SAMPLE_SITES = [
    {
        "site_id": "BLR001",
        "name": "Factory A - Main Boiler",
        "location": "Shah Alam, Malaysia"
    },
    {
        "site_id": "BLR002", 
        "name": "Factory B - Backup Boiler",
        "location": "Petaling Jaya, Malaysia"
    },
    {
        "site_id": "BLR003",
        "name": "Warehouse C - Steam Generator", 
        "location": "Subang Jaya, Malaysia"
    }
]

# Sample sensor configurations
SENSOR_CONFIGS = [
    {"sensor_type": "temperature", "unit": "celsius", "min_value": 60.0, "max_value": 120.0},
    {"sensor_type": "pressure", "unit": "bar", "min_value": 5.0, "max_value": 25.0},
    {"sensor_type": "fuel_level", "unit": "percentage", "min_value": 0.0, "max_value": 100.0},
    {"sensor_type": "flow_rate", "unit": "l/min", "min_value": 10.0, "max_value": 500.0},
    {"sensor_type": "efficiency", "unit": "percentage", "min_value": 70.0, "max_value": 95.0},
]

def generate_sensor_reading(sensor_config):
    """Generate a realistic sensor reading"""
    min_val = sensor_config["min_value"]
    max_val = sensor_config["max_value"]
    
    # Add some realistic variations
    if sensor_config["sensor_type"] == "temperature":
        # Temperature varies more during startup/shutdown
        base_temp = random.uniform(80, 95)
        variation = random.uniform(-5, 5)
        value = max(min_val, min(max_val, base_temp + variation))
    elif sensor_config["sensor_type"] == "pressure":
        # Pressure is usually stable
        base_pressure = random.uniform(10, 15)
        variation = random.uniform(-1, 1)
        value = max(min_val, min(max_val, base_pressure + variation))
    elif sensor_config["sensor_type"] == "fuel_level":
        # Fuel decreases over time
        value = random.uniform(20, 90)
    elif sensor_config["sensor_type"] == "efficiency":
        # Efficiency varies with operating conditions
        base_efficiency = random.uniform(85, 92)
        variation = random.uniform(-3, 3)
        value = max(min_val, min(max_val, base_efficiency + variation))
    else:
        # Default random within range
        value = random.uniform(min_val, max_val)
    
    return round(value, 2)

def send_sample_data(base_url="http://localhost"):
    """Send sample IoT data to the ingestion service"""
    
    print("🚀 Generating sample IoT data...")
    
    for site in SAMPLE_SITES:
        site_id = site["site_id"]
        
        # Generate readings for each sensor type
        readings = []
        for sensor_config in SENSOR_CONFIGS:
            value = generate_sensor_reading(sensor_config)
            readings.append({
                "sensor_type": sensor_config["sensor_type"],
                "value": value
            })
        
        # Prepare payload
        payload = {
            "site_id": site_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "readings": readings
        }
        
        # Send to IoT ingestion service
        try:
            url = f"{base_url}/api/iot/api/ingest/"
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {site_id}: Sent {result.get('processed_records', 0)} readings")
            else:
                print(f"❌ {site_id}: Error {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {site_id}: Connection error - {e}")

def generate_historical_data():
    """Generate sample historical data for analytics"""
    print("📊 Generating historical performance data...")
    
    # This would typically write to InfluxDB
    # For demo, we'll just generate sample data points
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    for site in SAMPLE_SITES:
        site_data = []
        current_date = start_date
        
        while current_date <= end_date:
            daily_readings = {}
            
            for sensor_config in SENSOR_CONFIGS:
                # Generate 24 hourly readings
                hourly_values = []
                for hour in range(24):
                    value = generate_sensor_reading(sensor_config)
                    hourly_values.append(value)
                
                daily_readings[sensor_config["sensor_type"]] = {
                    "average": round(sum(hourly_values) / len(hourly_values), 2),
                    "min": min(hourly_values),
                    "max": max(hourly_values),
                    "readings": hourly_values
                }
            
            site_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "site_id": site["site_id"],
                "data": daily_readings
            })
            
            current_date += timedelta(days=1)
        
        print(f"📈 Generated {len(site_data)} days of data for {site['site_id']}")

def create_sample_alerts():
    """Create sample alert rules"""
    print("🚨 Creating sample alert rules...")
    
    sample_rules = [
        {
            "site_id": "BLR001",
            "parameter": "temperature",
            "condition": "above",
            "threshold_max": 100.0,
            "severity": "high"
        },
        {
            "site_id": "BLR001", 
            "parameter": "pressure",
            "condition": "above",
            "threshold_max": 20.0,
            "severity": "critical"
        },
        {
            "site_id": "BLR002",
            "parameter": "fuel_level",
            "condition": "below", 
            "threshold_min": 15.0,
            "severity": "medium"
        }
    ]
    
    for rule in sample_rules:
        print(f"🔔 Alert rule: {rule['site_id']} - {rule['parameter']} {rule['condition']} threshold")

def main():
    """Main function to generate all sample data"""
    print("🏭 Boiler Monitoring Platform - Sample Data Generator")
    print("=" * 60)
    
    # Check if services are running
    try:
        response = requests.get("http://localhost/api/iot/health/", timeout=5)
        if response.status_code == 200:
            print("✅ IoT Ingestion service is running")
        else:
            print("⚠️  IoT Ingestion service responded with:", response.status_code)
    except requests.exceptions.RequestException:
        print("❌ Could not connect to IoT Ingestion service")
        print("   Make sure Docker containers are running: docker compose up")
        return
    
    print()
    
    # Generate and send sample data
    send_sample_data()
    print()
    
    generate_historical_data()
    print()
    
    create_sample_alerts()
    print()
    
    print("🎉 Sample data generation completed!")
    print("📊 You can now view the data in your dashboard at: http://localhost/")

if __name__ == "__main__":
    main()
