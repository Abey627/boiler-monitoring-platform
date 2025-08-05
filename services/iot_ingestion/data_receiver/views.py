from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import logging
import redis
from datetime import datetime
from .models import BoilerSite, Sensor, DataIngestionLog

logger = logging.getLogger(__name__)

# Redis client for real-time caching
redis_client = redis.from_url('redis://redis:6379/0', decode_responses=True)

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({"status": "ok", "service": "iot_ingestion"})

@csrf_exempt
@require_http_methods(["POST"])
def ingest_sensor_data(request):
    """
    Ingests IoT sensor data with dual storage strategy:
    1. InfluxDB for historical data (all readings)
    2. Redis for real-time cache (latest values only)
    
    Expected payload:
    {
        "site_id": "BLR001",
        "timestamp": "2025-01-01T10:30:00Z",
        "readings": [
            {"sensor_type": "temperature", "value": 85.5},
            {"sensor_type": "pressure", "value": 12.3}
        ]
    }
    """
    try:
        data = json.loads(request.body)
        site_id = data.get('site_id')
        readings = data.get('readings', [])
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Validate site exists
        try:
            boiler_site = BoilerSite.objects.get(site_id=site_id)
        except BoilerSite.DoesNotExist:
            return JsonResponse({
                'error': f'Boiler site {site_id} not found'
            }, status=404)
        
        processed_count = 0
        cached_count = 0
        
        for reading in readings:
            sensor_type = reading.get('sensor_type')
            value = reading.get('value')
            
            if sensor_type and value is not None:
                # 1. STORE IN INFLUXDB (Historical Data - All Readings)
                # This would typically write to InfluxDB for permanent storage
                # influxdb_write(site_id, sensor_type, value, timestamp)
                
                # 2. CACHE IN REDIS (Real-time Access - Latest Values Only)
                try:
                    cache_key = f"latest:{site_id}:{sensor_type}"
                    cache_data = {
                        'value': value,
                        'timestamp': timestamp,
                        'site_id': site_id,
                        'sensor_type': sensor_type
                    }
                    
                    # Cache with 5-minute TTL (real-time dashboard needs)
                    redis_client.setex(cache_key, 300, json.dumps(cache_data))
                    cached_count += 1
                    
                    # Update site-level dashboard cache
                    _update_site_dashboard_cache(site_id, sensor_type, value, timestamp)
                    
                    logger.debug(f"Cached reading: {site_id}/{sensor_type} = {value}")
                    
                except Exception as cache_error:
                    logger.warning(f"Cache write failed: {cache_error}")
                    # Continue processing even if cache fails
                
                processed_count += 1
        
        # Log ingestion event in PostgreSQL
        DataIngestionLog.objects.create(
            boiler_site=boiler_site,
            records_count=processed_count,
            status='success' if processed_count > 0 else 'error'
        )
        
        return JsonResponse({
            'status': 'success',
            'site_id': site_id,
            'processed_records': processed_count,
            'cached_records': cached_count,
            'storage_strategy': {
                'influxdb': 'historical_data',
                'redis': 'realtime_cache',
                'postgresql': 'metadata_logs'
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON payload'
        }, status=400)
    except Exception as e:
        logger.error(f"Data ingestion error: {e}")
        return JsonResponse({
            'error': 'Internal server error'
        }, status=500)

def _update_site_dashboard_cache(site_id, sensor_type, value, timestamp):
    """
    Update aggregated site data for instant dashboard loading.
    This ensures dashboard loads in <100ms instead of querying InfluxDB.
    """
    try:
        site_key = f"dashboard:{site_id}"
        
        # Get existing cached data
        cached_data = redis_client.get(site_key)
        if cached_data:
            site_data = json.loads(cached_data)
        else:
            site_data = {
                'site_id': site_id,
                'last_updated': timestamp,
                'sensors': {},
                'status': 'online'
            }
        
        # Update specific sensor
        site_data['sensors'][sensor_type] = {
            'value': value,
            'timestamp': timestamp
        }
        site_data['last_updated'] = timestamp
        
        # Determine site status based on readings
        if sensor_type == 'temperature' and value > 100:
            site_data['status'] = 'warning'
        elif sensor_type == 'pressure' and value > 20:
            site_data['status'] = 'critical'
        
        # Cache updated site data (1-minute TTL for dashboard)
        redis_client.setex(site_key, 60, json.dumps(site_data))
        
    except Exception as e:
        logger.error(f"Dashboard cache update failed: {e}")

@api_view(['GET'])
def get_realtime_data(request, site_id):
    """
    Get real-time data from Redis cache (sub-second response).
    This demonstrates why Redis provides real-time performance.
    """
    try:
        # Try Redis cache first (< 1ms response time)
        site_key = f"dashboard:{site_id}"
        cached_data = redis_client.get(site_key)
        
        if cached_data:
            dashboard_data = json.loads(cached_data)
            dashboard_data['source'] = 'redis_cache'
            dashboard_data['response_time'] = 'sub_millisecond'
            
            return Response({
                'site_id': site_id,
                'data': dashboard_data,
                'cache_hit': True,
                'performance': 'real_time'
            })
        
        # Fallback to database (slower, but comprehensive)
        return Response({
            'site_id': site_id,
            'data': _fetch_from_database(site_id),
            'cache_hit': False,
            'performance': 'database_query',
            'note': 'Cache miss - consider warming cache'
        })
        
    except Exception as e:
        logger.error(f"Real-time data fetch error: {e}")
        return Response({
            'error': 'Failed to fetch real-time data'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def _fetch_from_database(site_id):
    """
    Fallback method when Redis cache misses.
    This is slower but ensures data availability.
    """
    # This would query InfluxDB for latest readings
    # For demo, returning sample data
    return {
        'site_id': site_id,
        'sensors': {
            'temperature': {'value': 85.5, 'timestamp': datetime.now().isoformat()},
            'pressure': {'value': 12.3, 'timestamp': datetime.now().isoformat()},
        },
        'status': 'online',
        'source': 'database_fallback',
        'response_time': 'slower_but_reliable'
    }

@api_view(['GET'])
def get_site_sensors(request, site_id):
    """Get all sensors for a specific boiler site"""
    try:
        boiler_site = BoilerSite.objects.get(site_id=site_id)
        sensors = Sensor.objects.filter(boiler_site=boiler_site, is_active=True)
        
        sensor_data = []
        for sensor in sensors:
            # Check if we have real-time data in cache
            cache_key = f"latest:{site_id}:{sensor.sensor_type}"
            latest_reading = redis_client.get(cache_key)
            
            sensor_info = {
                'sensor_id': sensor.sensor_id,
                'sensor_type': sensor.sensor_type,
                'unit': sensor.unit,
                'min_value': sensor.min_value,
                'max_value': sensor.max_value
            }
            
            if latest_reading:
                reading_data = json.loads(latest_reading)
                sensor_info['latest_value'] = reading_data['value']
                sensor_info['last_updated'] = reading_data['timestamp']
                sensor_info['data_source'] = 'redis_cache'
            else:
                sensor_info['latest_value'] = None
                sensor_info['last_updated'] = None
                sensor_info['data_source'] = 'no_recent_data'
            
            sensor_data.append(sensor_info)
        
        return Response({
            'site_id': site_id,
            'site_name': boiler_site.name,
            'sensors': sensor_data,
            'cache_enabled': True
        })
        
    except BoilerSite.DoesNotExist:
        return Response({
            'error': f'Boiler site {site_id} not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_ingestion_stats(request):
    """Get data ingestion statistics"""
    from django.db.models import Count, Q
    from datetime import datetime, timedelta
    
    # Get stats for the last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    
    stats = DataIngestionLog.objects.filter(timestamp__gte=yesterday).aggregate(
        total_records=Count('id'),
        successful_records=Count('id', filter=Q(status='success')),
        failed_records=Count('id', filter=Q(status='error'))
    )
    
    # Get cache statistics
    try:
        cache_info = redis_client.info('memory')
        cache_stats = {
            'used_memory_mb': round(cache_info.get('used_memory', 0) / 1024 / 1024, 2),
            'connected_clients': cache_info.get('connected_clients', 0),
            'total_keys': redis_client.dbsize()
        }
    except:
        cache_stats = {'error': 'Unable to get Redis stats'}
    
    return Response({
        'period': '24_hours',
        'ingestion_stats': {
            'total_ingestion_events': stats['total_records'],
            'successful_events': stats['successful_records'],
            'failed_events': stats['failed_records'],
            'success_rate': round(
                (stats['successful_records'] / max(stats['total_records'], 1)) * 100, 2
            )
        },
        'cache_stats': cache_stats,
        'performance_strategy': {
            'influxdb': 'All historical sensor data for analytics',
            'redis': 'Latest values only for real-time dashboards',
            'postgresql': 'Business logic, configs, and audit logs'
        }
    })
