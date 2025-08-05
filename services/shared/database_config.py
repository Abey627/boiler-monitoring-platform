"""
Shared database configuration utilities for the boiler monitoring platform.
This module provides common database configurations that can be used across microservices.
"""

import os
from influxdb_client import InfluxDBClient
import redis
import logging

logger = logging.getLogger(__name__)

# PostgreSQL Configuration
def get_postgres_config():
    """Returns PostgreSQL database configuration for Django settings"""
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'steambytes_core'),
            'USER': os.getenv('POSTGRES_USER', 'steambytes'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'steambytes_dev_password'),
            'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 20,
            }
        }
    }

# InfluxDB Configuration
def get_influxdb_client():
    """Returns configured InfluxDB client"""
    url = os.getenv('INFLUX_URL', 'http://influxdb:8086')
    token = os.getenv('INFLUX_TOKEN', 'steambytes_admin_token')
    org = os.getenv('INFLUX_ORG', 'steambytes')
    
    try:
        client = InfluxDBClient(url=url, token=token, org=org)
        # Test connection
        client.ping()
        logger.info(f"InfluxDB connection established: {url}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to InfluxDB: {e}")
        return None

# Redis Configuration
def get_redis_client():
    """Returns configured Redis client"""
    redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    
    try:
        client = redis.from_url(redis_url, decode_responses=True)
        # Test connection
        client.ping()
        logger.info(f"Redis connection established: {redis_url}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None

# Time-Series Data Operations
class TimeSeriesManager:
    """Helper class for InfluxDB operations"""
    
    def __init__(self):
        self.client = get_influxdb_client()
        self.bucket = os.getenv('INFLUX_BUCKET', 'sensor_data')
        self.org = os.getenv('INFLUX_ORG', 'steambytes')
    
    def write_sensor_data(self, site_id, sensor_type, value, timestamp=None):
        """Write sensor data to InfluxDB"""
        if not self.client:
            logger.error("InfluxDB client not available")
            return False
        
        from influxdb_client.client.write_api import SYNCHRONOUS
        
        try:
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            
            point = {
                "measurement": "boiler_metrics",
                "tags": {
                    "site_id": site_id,
                    "sensor_type": sensor_type
                },
                "fields": {
                    "value": float(value)
                }
            }
            
            if timestamp:
                point["time"] = timestamp
            
            write_api.write(bucket=self.bucket, org=self.org, record=point)
            logger.debug(f"Wrote sensor data: {site_id}/{sensor_type} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to write sensor data: {e}")
            return False
    
    def query_latest_readings(self, site_id, hours=1):
        """Query latest sensor readings for a site"""
        if not self.client:
            return {}
        
        try:
            query_api = self.client.query_api()
            
            query = f'''
            from(bucket: "{self.bucket}")
            |> range(start: -{hours}h)
            |> filter(fn: (r) => r._measurement == "boiler_metrics")
            |> filter(fn: (r) => r.site_id == "{site_id}")
            |> last()
            |> yield(name: "latest")
            '''
            
            result = query_api.query(org=self.org, query=query)
            
            readings = {}
            for table in result:
                for record in table.records:
                    sensor_type = record.values.get('sensor_type')
                    value = record.values.get('_value')
                    timestamp = record.values.get('_time')
                    
                    readings[sensor_type] = {
                        'value': value,
                        'timestamp': timestamp
                    }
            
            return readings
            
        except Exception as e:
            logger.error(f"Failed to query latest readings: {e}")
            return {}

# Cache Operations
class CacheManager:
    """Helper class for Redis cache operations"""
    
    def __init__(self):
        self.client = get_redis_client()
    
    def cache_latest_reading(self, site_id, sensor_type, value, ttl=300):
        """Cache latest sensor reading"""
        if not self.client:
            return False
        
        try:
            key = f"latest:{site_id}:{sensor_type}"
            self.client.setex(key, ttl, value)
            return True
        except Exception as e:
            logger.error(f"Failed to cache reading: {e}")
            return False
    
    def get_cached_reading(self, site_id, sensor_type):
        """Get cached sensor reading"""
        if not self.client:
            return None
        
        try:
            key = f"latest:{site_id}:{sensor_type}"
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Failed to get cached reading: {e}")
            return None
    
    def cache_dashboard_data(self, user_id, data, ttl=60):
        """Cache dashboard data for a user"""
        if not self.client:
            return False
        
        try:
            import json
            key = f"dashboard:{user_id}"
            self.client.setex(key, ttl, json.dumps(data))
            return True
        except Exception as e:
            logger.error(f"Failed to cache dashboard data: {e}")
            return False
