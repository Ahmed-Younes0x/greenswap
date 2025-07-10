from functools import wraps
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from .models import SecurityLog
from .utils import get_client_ip, block_ip

def rate_limit(max_requests=60, window=60, block_duration=300):
    """ديكوريتر لتحديد معدل الطلبات"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            ip = get_client_ip(request)
            cache_key = f"rate_limit_{ip}_{view_func.__name__}"
            
            current_requests = cache.get(cache_key, 0)
            
            if current_requests >= max_requests:
                # حظر IP مؤقتاً
                block_ip(ip, block_duration)
                
                # تسجيل الحدث
                SecurityLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    event_type='rate_limit_exceeded',
                    severity='medium',
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    details={
                        'view': view_func.__name__,
                        'max_requests': max_requests,
                        'window': window
                    }
                )
                
                return JsonResponse({
                    'error': 'تم تجاوز حد الطلبات المسموح',
                    'retry_after': block_duration
                }, status=429)
            
            cache.set(cache_key, current_requests + 1, window)
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator

def require_2fa(view_func):
    """ديكوريتر يتطلب المصادقة الثنائية"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        from .models import TwoFactorAuth
        
        try:
            two_fa = TwoFactorAuth.objects.get(user=request.user, is_enabled=True)
            
            # التحقق من وجود جلسة 2FA صالحة
            session_key = f"2fa_verified_{request.user.id}"
            if not request.session.get(session_key):
                return JsonResponse({
                    'error': 'المصادقة الثنائية مطلوبة',
                    'requires_2fa': True
                }, status=403)
                
        except TwoFactorAuth.DoesNotExist:
            pass  # المصادقة الثنائية غير مفعلة
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def log_security_event(event_type, severity='low'):
    """ديكوريتر لتسجيل الأحداث الأمنية"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                response = view_func(request, *args, **kwargs)
                
                # تسجيل الحدث
                SecurityLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    event_type=event_type,
                    severity=severity,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    details={
                        'view': view_func.__name__,
                        'method': request.method,
                        'path': request.path,
                        'status_code': getattr(response, 'status_code', 200)
                    }
                )
                
                return response
                
            except Exception as e:
                # تسجيل الخطأ
                SecurityLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    event_type='error',
                    severity='high',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    details={
                        'view': view_func.__name__,
                        'error': str(e)
                    }
                )
                raise
        
        return wrapper
    return decorator

def validate_input(validator_func):
    """ديكوريتر للتحقق من صحة المدخلات"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                # التحقق من البيانات
                if request.method in ['POST', 'PUT', 'PATCH']:
                    data = request.POST.dict() if hasattr(request, 'POST') else {}
                    validator_func(data)
                
                return view_func(request, *args, **kwargs)
                
            except ValidationError as e:
                return JsonResponse({
                    'error': 'بيانات غير صحيحة',
                    'details': str(e)
                }, status=400)
        
        return wrapper
    return decorator

def require_api_key(permissions=None):
    """ديكوريتر يتطلب مفتاح API"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from .models import APIKey
            
            api_key = request.META.get('HTTP_X_API_KEY')
            if not api_key:
                return JsonResponse({
                    'error': 'مفتاح API مطلوب'
                }, status=401)
            
            try:
                key_obj = APIKey.objects.get(key=api_key, is_active=True)
                
                # فحص الصلاحيات
                if permissions:
                    if not any(perm in key_obj.permissions for perm in permissions):
                        return JsonResponse({
                            'error': 'صلاحيات غير كافية'
                        }, status=403)
                
                # إضافة معلومات المفتاح للطلب
                request.api_key = key_obj
                request.user = key_obj.user
                
                return view_func(request, *args, **kwargs)
                
            except APIKey.DoesNotExist:
                return JsonResponse({
                    'error': 'مفتاح API غير صحيح'
                }, status=401)
        
        return wrapper
    return decorator
