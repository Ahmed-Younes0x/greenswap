import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse
from .models import QueryPerformance

logger = logging.getLogger('performance')

class PerformanceMiddleware(MiddlewareMixin):
    """مراقبة أداء الطلبات"""
    
    def process_request(self, request):
        request._performance_start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, '_performance_start_time'):
            duration = time.time() - request._performance_start_time
            
            # تسجيل الطلبات البطيئة
            if duration > 1.0:  # أكثر من ثانية
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.3f}s"
                )
            
            # إضافة header للأداء
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response

class CompressionMiddleware(MiddlewareMixin):
    """ضغط الاستجابات"""
    
    def process_response(self, request, response):
        # تطبيق ضغط للاستجابات الكبيرة
        if (hasattr(response, 'content') and 
            len(response.content) > 1024 and  # أكبر من 1KB
            'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', '')):
            
            import gzip
            compressed_content = gzip.compress(response.content)
            
            if len(compressed_content) < len(response.content):
                response.content = compressed_content
                response['Content-Encoding'] = 'gzip'
                response['Content-Length'] = str(len(compressed_content))
        
        return response

class CacheControlMiddleware(MiddlewareMixin):
    """إدارة cache headers"""
    
    def process_response(self, request, response):
        # إعداد cache headers للملفات الثابتة
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=31536000'  # سنة واحدة
            response['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
        
        # إعداد cache headers للـ API
        elif request.path.startswith('/api/'):
            if request.method == 'GET':
                response['Cache-Control'] = 'public, max-age=300'  # 5 دقائق
            else:
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        
        return response
