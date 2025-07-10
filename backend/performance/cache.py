import hashlib
import json
import pickle
from typing import Any, Optional, Union, List
from django.core.cache import cache
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone
from datetime import timedelta
import redis
import logging

logger = logging.getLogger('performance')

class AdvancedCache:
    """نظام كاش متقدم مع Redis"""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.default_timeout = getattr(settings, 'CACHE_DEFAULT_TIMEOUT', 3600)
        
    def generate_key(self, prefix: str, *args, **kwargs) -> str:
        """توليد مفتاح كاش فريد"""
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return f"{prefix}:{hashlib.md5(key_string.encode()).hexdigest()}"
    
    def get(self, key: str, default=None) -> Any:
        """استرجاع من الكاش مع تسجيل الإحصائيات"""
        try:
            value = cache.get(key, default)
            self._update_stats(key, hit=value is not None)
            return value
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return default
    
    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """حفظ في الكاش"""
        try:
            timeout = timeout or self.default_timeout
            return cache.set(key, value, timeout)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """حذف من الكاش"""
        try:
            return cache.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def get_or_set(self, key: str, callable_func, timeout: Optional[int] = None) -> Any:
        """استرجاع أو تعيين قيمة جديدة"""
        value = self.get(key)
        if value is None:
            value = callable_func()
            self.set(key, value, timeout)
        return value
    
    def invalidate_pattern(self, pattern: str) -> int:
        """حذف جميع المفاتيح التي تطابق النمط"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache invalidate pattern error for {pattern}: {e}")
            return 0
    
    def _update_stats(self, key: str, hit: bool):
        """تحديث إحصائيات الكاش"""
        from .models import CacheStats
        try:
            stats, created = CacheStats.objects.get_or_create(key=key)
            if hit:
                stats.hits += 1
            else:
                stats.misses += 1
            stats.save(update_fields=['hits', 'misses', 'last_accessed'])
        except Exception as e:
            logger.error(f"Cache stats update error: {e}")

# إنشاء instance عام
advanced_cache = AdvancedCache()

class QueryCache:
    """كاش خاص بالاستعلامات"""
    
    @staticmethod
    def cache_queryset(queryset: QuerySet, timeout: int = 3600) -> List:
        """كاش نتائج QuerySet"""
        key = QueryCache._generate_queryset_key(queryset)
        cached_result = advanced_cache.get(key)
        
        if cached_result is None:
            # تحويل QuerySet إلى قائمة وحفظها
            result = list(queryset)
            advanced_cache.set(key, result, timeout)
            return result
        
        return cached_result
    
    @staticmethod
    def _generate_queryset_key(queryset: QuerySet) -> str:
        """توليد مفتاح للـ QuerySet"""
        query_str = str(queryset.query)
        model_name = queryset.model._meta.label
        return advanced_cache.generate_key('queryset', model_name, query_str)
    
    @staticmethod
    def invalidate_model_cache(model_class):
        """إلغاء كاش نموذج معين"""
        model_name = model_class._meta.label
        pattern = f"queryset:*{model_name}*"
        return advanced_cache.invalidate_pattern(pattern)

class ViewCache:
    """كاش خاص بالـ Views"""
    
    @staticmethod
    def cache_view_response(view_name: str, request_data: dict, response_data: Any, timeout: int = 1800):
        """كاش استجابة View"""
        key = advanced_cache.generate_key('view', view_name, **request_data)
        advanced_cache.set(key, response_data, timeout)
    
    @staticmethod
    def get_cached_view_response(view_name: str, request_data: dict) -> Optional[Any]:
        """استرجاع استجابة View المحفوظة"""
        key = advanced_cache.generate_key('view', view_name, **request_data)
        return advanced_cache.get(key)
