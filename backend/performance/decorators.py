import time
import functools
import hashlib
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .cache import advanced_cache, ViewCache
from .models import QueryPerformance
import logging

logger = logging.getLogger('performance')

def cache_result(timeout=3600, key_prefix=''):
    """ديكوريتر لكاش نتائج الدوال"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # توليد مفتاح فريد
            key = advanced_cache.generate_key(
                key_prefix or func.__name__,
                *args,
                **kwargs
            )
            
            # محاولة استرجاع من الكاش
            result = advanced_cache.get(key)
            if result is not None:
                return result
            
            # تنفيذ الدالة وحفظ النتيجة
            result = func(*args, **kwargs)
            advanced_cache.set(key, result, timeout)
            return result
        
        return wrapper
    return decorator

def cache_api_response(timeout=1800):
    """ديكوريتر لكاش استجابات API"""
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # تجاهل الكاش للطلبات غير GET
            if request.method != 'GET':
                return view_func(request, *args, **kwargs)
            
            # إنشاء مفتاح كاش
            cache_key_data = {
                'view': view_func.__name__,
                'args': args,
                'kwargs': kwargs,
                'query_params': dict(request.GET),
                'user_id': getattr(request.user, 'id', None)
            }
            
            cached_response = ViewCache.get_cached_view_response(
                view_func.__name__, 
                cache_key_data
            )
            
            if cached_response:
                return JsonResponse(cached_response)
            
            # تنفيذ View وحفظ النتيجة
            response = view_func(request, *args, **kwargs)
            
            if hasattr(response, 'data') and response.status_code == 200:
                ViewCache.cache_view_response(
                    view_func.__name__,
                    cache_key_data,
                    response.data,
                    timeout
                )
            
            return response
        
        return wrapper
    return decorator

def monitor_query_performance(func):
    """مراقبة أداء الاستعلامات"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # تسجيل الأداء إذا كان بطيئاً
            if execution_time > 0.1:  # أكثر من 100ms
                QueryPerformance.objects.create(
                    query_hash=hashlib.md5(str(func).encode()).hexdigest(),
                    query_sql=str(func.__name__),
                    execution_time=execution_time,
                    table_name=getattr(func, '__qualname__', 'unknown')
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Query performance monitoring error: {e}")
            raise
    
    return wrapper

def smart_cache_page(timeout=3600):
    """كاش صفحة ذكي مع تنويع حسب المستخدم"""
    def decorator(view_func):
        @cache_page(timeout)
        @vary_on_headers('User-Agent', 'Accept-Language')
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
