import time
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .services import AnalyticsService, PerformanceMonitoringService, ErrorTrackingService
import logging

logger = logging.getLogger('analytics')

class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware لتتبع التحليلات تلقائياً"""
    
    def process_request(self, request):
        """بداية معالجة الطلب"""
        request._analytics_start_time = time.time()
        
        # تتبع مشاهدة الصفحة
        if request.method == 'GET' and not request.path.startswith('/api/'):
            AnalyticsService.track_event(
                event_type='page_view',
                event_name='page_view',
                user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                session_id=request.session.session_key,
                properties={
                    'path': request.path,
                    'method': request.method
                },
                request=request
            )
    
    def process_response(self, request, response):
        """نهاية معالجة الطلب"""
        if hasattr(request, '_analytics_start_time'):
            # حساب وقت الاستجابة
            response_time = (time.time() - request._analytics_start_time) * 1000  # بالميلي ثانية
            
            # تسجيل مقياس الأداء
            PerformanceMonitoringService.record_metric(
                metric_type='api_response_time' if request.path.startswith('/api/') else 'page_load_time',
                metric_name=request.path,
                value=response_time,
                tags={
                    'method': request.method,
                    'status_code': response.status_code,
                    'user_authenticated': hasattr(request, 'user') and request.user.is_authenticated
                }
            )
            
            # تتبع الأخطاء
            if response.status_code >= 400:
                ErrorTrackingService.log_error(
                    level='error' if response.status_code >= 500 else 'warning',
                    message=f"HTTP {response.status_code} - {request.path}",
                    user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                    request=request,
                    extra_data={
                        'status_code': response.status_code,
                        'response_time': response_time
                    }
                )
        
        return response
    
    def process_exception(self, request, exception):
        """معالجة الاستثناءات"""
        ErrorTrackingService.log_error(
            level='critical',
            message=str(exception),
            exception=exception,
            user=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
            request=request
        )
        
        return None
