"""
Real-time caching strategy for IoT boiler monitoring platform.
This demonstrates how Redis provides real-time performance without storing all data.
"""

import redis
import json
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient
import logging

logger = logging.getLogger(__name__)

class RealTimeCache:
    """
    Redis-based caching for real-time dashboard performance.
    Stores only latest values and frequently accessed data.
    """
    
    def __init__(self):
        self.redis_client = redis.from_url('redis://redis:6379/0', decode_responses=True)
        self.cache_ttl = {
            'latest_readings': 300,    # 5 minutes
            'dashboard_data': 60,      # 1 minute
            'alert_counts': 30,        # 30 seconds
            'site_status': 120,        # 2 minutes
        }
    
    def cache_latest_reading(self, site_id, sensor_type, value, timestamp=None):
        """
        Cache ONLY the latest sensor reading - not historical data
        This enables instant dashboard updates
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # Cache individual sensor reading
        key = f"latest:{site_id}:{sensor_type}"
        data = {
            'value': value,
            'timestamp': timestamp,
            'site_id': site_id,
            'sensor_type': sensor_type
        }
        
        self.redis_client.setex(
            key, 
            self.cache_ttl['latest_readings'], 
            json.dumps(data)
        )
        
        # Update site-level cache for dashboard
        self._update_site_dashboard_cache(site_id, sensor_type, value)
        
        logger.debug(f"Cached latest reading: {site_id}/{sensor_type} = {value}")
    
    def _update_site_dashboard_cache(self, site_id, sensor_type, value):
        """
        Update aggregated site data for instant dashboard loading
        """
        site_key = f"dashboard:{site_id}"
        
        # Get existing cached data
        cached_data = self.redis_client.get(site_key)
        if cached_data:
            site_data = json.loads(cached_data)
        else:
            site_data = {
                'site_id': site_id,
                'last_updated': datetime.now().isoformat(),
                'sensors': {},
                'status': 'online'
            }
        
        # Update specific sensor
        site_data['sensors'][sensor_type] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        site_data['last_updated'] = datetime.now().isoformat()
        
        # Cache updated site data
        self.redis_client.setex(
            site_key,
            self.cache_ttl['dashboard_data'],
            json.dumps(site_data)
        )
    
    def get_dashboard_data(self, site_id):
        """
        Get real-time dashboard data from cache (sub-millisecond response)
        Falls back to database if cache miss
        """
        site_key = f"dashboard:{site_id}"
        cached_data = self.redis_client.get(site_key)
        
        if cached_data:
            logger.debug(f"Dashboard cache HIT for {site_id}")
            return json.loads(cached_data)
        
        logger.debug(f"Dashboard cache MISS for {site_id} - fetching from DB")
        # Fallback: fetch from InfluxDB (slower but comprehensive)
        return self._fetch_from_influxdb(site_id)
    
    def _fetch_from_influxdb(self, site_id):
        """
        Fallback method to fetch data from InfluxDB when cache misses
        This is slower but ensures data availability
        """
        # This would connect to InfluxDB and fetch latest readings
        # For demo purposes, returning sample data
        return {
            'site_id': site_id,
            'last_updated': datetime.now().isoformat(),
            'sensors': {
                'temperature': {'value': 85.5, 'timestamp': datetime.now().isoformat()},
                'pressure': {'value': 12.3, 'timestamp': datetime.now().isoformat()},
            },
            'status': 'online',
            'source': 'influxdb_fallback'
        }

class AlertQueue:
    """
    Redis-based alert processing queue for real-time notifications
    """
    
    def __init__(self):
        self.redis_client = redis.from_url('redis://redis:6379/0', decode_responses=True)
        self.queue_key = "alerts:processing_queue"
    
    def queue_alert(self, alert_data):
        """
        Queue alert for immediate processing (real-time notifications)
        """
        alert_payload = {
            'alert_id': alert_data.get('alert_id'),
            'site_id': alert_data.get('site_id'),
            'severity': alert_data.get('severity'),
            'message': alert_data.get('message'),
            'timestamp': datetime.now().isoformat(),
            'status': 'queued'
        }
        
        # Add to Redis queue for immediate processing
        self.redis_client.lpush(self.queue_key, json.dumps(alert_payload))
        
        # Set expiration for queue cleanup (24 hours)
        self.redis_client.expire(self.queue_key, 86400)
        
        logger.info(f"Queued alert: {alert_data.get('site_id')} - {alert_data.get('severity')}")
    
    def process_alert_queue(self):
        """
        Process alerts from queue (would be called by background worker)
        """
        while True:
            # Block until alert available (real-time processing)
            alert_data = self.redis_client.brpop(self.queue_key, timeout=1)
            
            if alert_data:
                _, alert_json = alert_data
                alert = json.loads(alert_json)
                
                # Process alert (send email, SMS, webhook, etc.)
                self._send_notification(alert)
            else:
                break
    
    def _send_notification(self, alert):
        """Send alert notification"""
        logger.info(f"Sending notification: {alert['site_id']} - {alert['message']}")
        # Implementation would send actual notifications

class SessionManager:
    """
    Redis-based session management for real-time user experience
    """
    
    def __init__(self):
        self.redis_client = redis.from_url('redis://redis:6379/0', decode_responses=True)
    
    def cache_user_dashboard(self, user_id, dashboard_config):
        """
        Cache user's dashboard configuration for instant loading
        """
        key = f"user_dashboard:{user_id}"
        self.redis_client.setex(key, 1800, json.dumps(dashboard_config))  # 30 minutes
    
    def get_user_dashboard(self, user_id):
        """
        Get user dashboard config from cache (instant loading)
        """
        key = f"user_dashboard:{user_id}"
        cached_config = self.redis_client.get(key)
        
        if cached_config:
            return json.loads(cached_config)
        return None

# Example usage demonstrating the real-time flow
def example_iot_data_flow():
    """
    Example showing how data flows for real-time performance
    """
    cache = RealTimeCache()
    alert_queue = AlertQueue()
    
    # 1. Sensor sends reading
    site_id = "BLR001"
    temperature = 95.5  # High temperature
    
    # 2. Store in InfluxDB (permanent storage) - slower write
    # influxdb_client.write_sensor_data(site_id, 'temperature', temperature)
    
    # 3. Cache latest value in Redis (instant dashboard updates)
    cache.cache_latest_reading(site_id, 'temperature', temperature)
    
    # 4. Check for alerts (using cached thresholds)
    if temperature > 90:  # Alert threshold
        alert_queue.queue_alert({
            'alert_id': f"TEMP_{site_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'site_id': site_id,
            'severity': 'high',
            'message': f'High temperature detected: {temperature}°C'
        })
    
    # 5. Dashboard requests data (instant response from Redis)
    dashboard_data = cache.get_dashboard_data(site_id)
    print(f"Dashboard data (real-time): {dashboard_data}")

if __name__ == "__main__":
    example_iot_data_flow()
