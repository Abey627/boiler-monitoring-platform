from django.db import models
from django.utils import timezone

class AnalyticsJob(models.Model):
    """Tracks analytics processing jobs"""
    JOB_TYPES = [
        ('efficiency_analysis', 'Efficiency Analysis'),
        ('predictive_maintenance', 'Predictive Maintenance'),
        ('anomaly_detection', 'Anomaly Detection'),
        ('trend_analysis', 'Trend Analysis'),
        ('cost_optimization', 'Cost Optimization'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    job_id = models.CharField(max_length=100, unique=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    site_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parameters = models.JSONField()  # Job-specific parameters
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job_type} - {self.site_id} - {self.status}"

class PredictiveModel(models.Model):
    """Stores trained ML models for predictive analytics"""
    MODEL_TYPES = [
        ('efficiency', 'Efficiency Prediction'),
        ('maintenance', 'Maintenance Prediction'),
        ('failure', 'Failure Prediction'),
        ('consumption', 'Fuel Consumption'),
    ]
    
    name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    version = models.CharField(max_length=20)
    site_id = models.CharField(max_length=50)
    model_data = models.JSONField()  # Serialized model or model parameters
    accuracy_score = models.FloatField(null=True, blank=True)
    training_data_period = models.CharField(max_length=100)  # e.g., "2024-01 to 2024-12"
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['site_id', 'model_type', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version} - {self.site_id}"

class AnalyticsResult(models.Model):
    """Stores results from analytics processing"""
    RESULT_TYPES = [
        ('efficiency_score', 'Efficiency Score'),
        ('maintenance_prediction', 'Maintenance Prediction'),
        ('anomaly_detection', 'Anomaly Detection'),
        ('cost_savings', 'Cost Savings Opportunity'),
    ]
    
    site_id = models.CharField(max_length=50)
    result_type = models.CharField(max_length=50, choices=RESULT_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.FloatField()
    confidence = models.FloatField(null=True, blank=True)  # Confidence score (0-1)
    metadata = models.JSONField(blank=True, null=True)  # Additional result data
    model_used = models.ForeignKey(PredictiveModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.site_id} - {self.result_type} - {self.timestamp}"

class PerformanceMetric(models.Model):
    """Tracks calculated performance metrics"""
    METRIC_TYPES = [
        ('overall_efficiency', 'Overall Efficiency'),
        ('fuel_consumption_rate', 'Fuel Consumption Rate'),
        ('uptime_percentage', 'Uptime Percentage'),
        ('maintenance_cost', 'Maintenance Cost'),
        ('energy_savings', 'Energy Savings'),
    ]
    
    site_id = models.CharField(max_length=50)
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    period = models.CharField(max_length=20)  # 'daily', 'weekly', 'monthly'
    date = models.DateField()
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    baseline_value = models.FloatField(null=True, blank=True)
    improvement_percentage = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ['site_id', 'metric_type', 'period', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.site_id} - {self.metric_type} - {self.date}"
