from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from datetime import timedelta

class CacheStats(models.Model):
    """إحصائيات الكاش"""
    key = models.CharField(max_length=255, unique=True)
    hits = models.PositiveIntegerField(default=0)
    misses = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0

    def __str__(self):
        return f"{self.key} - Hit Rate: {self.hit_rate:.2f}%"

class QueryPerformance(models.Model):
    """مراقبة أداء الاستعلامات"""
    query_hash = models.CharField(max_length=64, db_index=True)
    query_sql = models.TextField()
    execution_time = models.FloatField()
    table_name = models.CharField(max_length=100, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['query_hash', 'timestamp']),
            models.Index(fields=['table_name', 'execution_time']),
        ]

    def __str__(self):
        return f"{self.table_name} - {self.execution_time:.3f}s"

class CDNStats(models.Model):
    """إحصائيات CDN"""
    file_path = models.CharField(max_length=500)
    file_size = models.PositiveIntegerField()
    requests_count = models.PositiveIntegerField(default=0)
    bandwidth_used = models.BigIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['file_path']),
            models.Index(fields=['last_accessed']),
        ]

    def __str__(self):
        return f"{self.file_path} - {self.requests_count} requests"
