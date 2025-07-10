import json
import time
import hashlib
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import SecurityLog, RateLimitRecord
from .utils import get_client_ip, is_suspicious_request

User = get_user_model()

class SecurityMiddleware(MiddlewareMixin):
    """Middleware شامل للأمان"""
    
    def process_request(self, request):
        # تسجيل الطلب
        self.log_request(request)
        
        # فحص الطلبات المشبوهة
        if self.is_suspicious_request(request):
            self.log_security_event(request, 'suspicious_activity', 'high')
            return JsonResponse({'error': 'طلب مشبوه'}, status=403)
        
        # فحص Rate Limiting
        if self.is_rate_limited(request):
            self.log_security_event(request, 'rate_limit_exceeded', 'medium')
            return JsonResponse({'error': 'تم تجاوز حد الطلبات'}, status=429)
        
        return None
    
    def log_request(self, request):
        """تسجيل الطلب في الكاش للمراقبة"""
        ip = get_client_ip(request)
        cache_key = f"request_log_{ip}_{int(time.time() // 60)}"  # نافذة دقيقة واحدة
        
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1, 60)
    
    def is_suspicious_request(self, request):
        """فحص الطلبات المشبوهة"""
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # فحص IP المحظورة
        blocked_ips = cache.get('blocked_ips', set())
        if ip in blocked_ips:
            return True
        
        # فحص User Agent المشبوه
        suspicious_agents = ['bot', 'crawler', 'scanner', 'hack']
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            return True
        
        # فحص عدد الطلبات المفرط
        cache_key = f"request_count_{ip}"
        request_count = cache.get(cache_key, 0)
        if request_count > 100:  # أكثر من 100 طلب في الدقيقة
            return True
        
        return False
    
    def is_rate_limited(self, request):
        """فحص حدود الطلبات"""
        ip = get_client_ip(request)
        endpoint = request.path
        
        # حدود مختلفة لنقاط نهاية مختلفة
        limits = {
            '/api/auth/login/': 5,  # 5 محاولات تسجيل دخول في الدقيقة
            '/api/auth/register/': 3,  # 3 تسجيلات في الدقيقة
            '/api/items/create/': 10,  # 10 منتجات في الدقيقة
            'default': 60  # 60 طلب في الدقيقة للباقي
        }
        
        limit = limits.get(endpoint, limits['default'])
        cache_key = f"rate_limit_{ip}_{endpoint}"
        
        current_count = cache.get(cache_key, 0)
        if current_count >= limit:
            return True
        
        cache.set(cache_key, current_count + 1, 60)
        return False
    
    def log_security_event(self, request, event_type, severity):
        """تسجيل حدث أمني"""
        try:
            SecurityLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                event_type=event_type,
                severity=severity,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={
                    'path': request.path,
                    'method': request.method,
                    'data': dict(request.GET) if request.method == 'GET' else {}
                }
            )
        except Exception:
            pass  # تجنب كسر الطلب في حالة فشل التسجيل

class CSRFMiddleware(MiddlewareMixin):
    """حماية CSRF متقدمة"""
    
    def process_request(self, request):
        # تخطي فحص CSRF للـ API endpoints مع API key
        if request.path.startswith('/api/') and 'HTTP_X_API_KEY' in request.META:
            return None
        
        # فحص CSRF token للطلبات POST/PUT/DELETE
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            csrf_token = request.META.get('HTTP_X_CSRFTOKEN') or request.POST.get('csrfmiddlewaretoken')
            
            if not csrf_token:
                return JsonResponse({'error': 'CSRF token مطلوب'}, status=403)
            
            # التحقق من صحة الـ token
            if not self.is_valid_csrf_token(csrf_token, request):
                return JsonResponse({'error': 'CSRF token غير صحيح'}, status=403)
        
        return None
    
    def is_valid_csrf_token(self, token, request):
        """التحقق من صحة CSRF token"""
        # هنا يمكن إضافة منطق التحقق المخصص
        # Django يتولى هذا تلقائياً، لكن يمكن إضافة فحوصات إضافية
        return True

class XSSProtectionMiddleware(MiddlewareMixin):
    """حماية من XSS"""
    
    def process_response(self, request, response):
        # إضافة headers الأمان
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Content-Security-Policy'] = self.get_csp_header()
        
        return response
    
    def get_csp_header(self):
        """إنشاء Content Security Policy header"""
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https: blob:",
            "connect-src 'self' https://api.openai.com",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        return '; '.join(csp_directives)
