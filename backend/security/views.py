from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import APIKey, TwoFactorAuth, SecurityLog
from .serializers import (
    APIKeySerializer, TwoFactorSetupSerializer, 
    SecurityLogSerializer, ChangePasswordSerializer
)
from .authentication import TwoFactorAuthService
from .decorators import rate_limit, require_2fa, log_security_event
from .utils import get_client_ip

class APIKeyListCreateView(generics.ListCreateAPIView):
    """إدارة مفاتيح API"""
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class APIKeyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """تفاصيل مفتاح API"""
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@rate_limit(max_requests=5, window=300)  # 5 محاولات كل 5 دقائق
def setup_2fa(request):
    """إعداد المصادقة الثنائية"""
    try:
        setup_data = TwoFactorAuthService.setup_2fa(request.user)
        return Response({
            'success': True,
            'data': setup_data,
            'message': 'تم إعداد المصادقة الثنائية. امسح رمز QR بتطبيق المصادقة'
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@rate_limit(max_requests=10, window=300)
def enable_2fa(request):
    """تفعيل المصادقة الثنائية"""
    otp_code = request.data.get('otp_code')
    if not otp_code:
        return Response({
            'error': 'كود OTP مطلوب'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if TwoFactorAuthService.enable_2fa(request.user, otp_code):
        return Response({
            'success': True,
            'message': 'تم تفعيل المصادقة الثنائية بنجاح'
        })
    else:
        return Response({
            'success': False,
            'error': 'كود OTP غير صحيح'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@require_2fa
def disable_2fa(request):
    """إلغاء تفعيل المصادقة الثنائية"""
    password = request.data.get('password')
    if not password:
        return Response({
            'error': 'كلمة المرور مطلوبة'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if TwoFactorAuthService.disable_2fa(request.user, password):
        return Response({
            'success': True,
            'message': 'تم إلغاء تفعيل المصادقة الثنائية'
        })
    else:
        return Response({
            'success': False,
            'error': 'كلمة المرور غير صحيحة'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@rate_limit(max_requests=5, window=300)
def verify_2fa_login(request):
    """التحقق من تسجيل الدخول بالمصادقة الثنائية"""
    username = request.data.get('username')
    password = request.data.get('password')
    otp_code = request.data.get('otp_code')
    
    if not all([username, password, otp_code]):
        return Response({
            'error': 'جميع الحقول مطلوبة'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(
        request=request,
        username=username,
        password=password,
        otp_code=otp_code
    )
    
    if user:
        login(request, user)
        # تعيين جلسة 2FA
        request.session[f"2fa_verified_{user.id}"] = True
        
        return Response({
            'success': True,
            'message': 'تم تسجيل الدخول بنجاح',
            'user_id': user.id
        })
    else:
        return Response({
            'success': False,
            'error': 'بيانات تسجيل الدخول غير صحيحة'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_2fa_status(request):
    """الحصول على حالة المصادقة الثنائية"""
    try:
        two_fa = TwoFactorAuth.objects.get(user=request.user)
        return Response({
            'is_enabled': two_fa.is_enabled,
            'backup_codes_count': len(two_fa.backup_codes),
            'last_used': two_fa.last_used
        })
    except TwoFactorAuth.DoesNotExist:
        return Response({
            'is_enabled': False,
            'backup_codes_count': 0,
            'last_used': None
        })

class SecurityLogListView(generics.ListAPIView):
    """عرض سجلات الأمان للمستخدم"""
    serializer_class = SecurityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SecurityLog.objects.filter(user=self.request.user).order_by('-timestamp')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@rate_limit(max_requests=3, window=300)
@log_security_event('password_change', 'medium')
def change_password(request):
    """تغيير كلمة المرور"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # التحقق من كلمة المرور الحالية
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'كلمة المرور الحالية غير صحيحة'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # تعيين كلمة المرور الجديدة
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'تم تغيير كلمة المرور بنجاح'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_security_dashboard(request):
    """لوحة معلومات الأمان"""
    user = request.user
    
    # إحصائيات الأمان
    recent_logs = SecurityLog.objects.filter(user=user).order_by('-timestamp')[:10]
    failed_logins = recent_logs.filter(event_type='failed_login').count()
    
    # معلومات المصادقة الثنائية
    two_fa_enabled = TwoFactorAuth.objects.filter(user=user, is_enabled=True).exists()
    
    # مفاتيح API النشطة
    active_api_keys = APIKey.objects.filter(user=user, is_active=True).count()
    
    # آخر عنوان IP
    last_login_ip = recent_logs.filter(event_type='login_attempt').first()
    last_ip = last_login_ip.ip_address if last_login_ip else None
    
    return Response({
        'security_score': calculate_security_score(user),
        'two_fa_enabled': two_fa_enabled,
        'active_api_keys': active_api_keys,
        'recent_failed_logins': failed_logins,
        'last_login_ip': last_ip,
        'recent_activities': SecurityLogSerializer(recent_logs, many=True).data,
        'recommendations': get_security_recommendations(user)
    })

def calculate_security_score(user):
    """حساب نقاط الأمان للمستخدم"""
    score = 0
    
    # كلمة مرور قوية (30 نقطة)
    if len(user.password) > 60:  # Django hashed password
        score += 30
    
    # المصادقة الثنائية (40 نقطة)
    if TwoFactorAuth.objects.filter(user=user, is_enabled=True).exists():
        score += 40
    
    # عدم وجود محاولات فشل حديثة (20 نقطة)
    recent_failures = SecurityLog.objects.filter(
        user=user,
        event_type='failed_login',
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    if recent_failures == 0:
        score += 20
    elif recent_failures < 3:
        score += 10
    
    # تحديث كلمة المرور حديثاً (10 نقاط)
    if user.date_joined > timezone.now() - timedelta(days=90):
        score += 10
    
    return min(score, 100)

def get_security_recommendations(user):
    """الحصول على توصيات الأمان"""
    recommendations = []
    
    # المصادقة الثنائية
    if not TwoFactorAuth.objects.filter(user=user, is_enabled=True).exists():
        recommendations.append({
            'type': 'enable_2fa',
            'title': 'فعل المصادقة الثنائية',
            'description': 'زد من أمان حسابك بتفعيل المصادقة الثنائية',
            'priority': 'high'
        })
    
    # محاولات فشل حديثة
    recent_failures = SecurityLog.objects.filter(
        user=user,
        event_type='failed_login',
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    if recent_failures > 5:
        recommendations.append({
            'type': 'check_account',
            'title': 'فحص الحساب',
            'description': f'تم رصد {recent_failures} محاولة فشل في تسجيل الدخول',
            'priority': 'high'
        })
    
    # تحديث كلمة المرور
    if user.date_joined < timezone.now() - timedelta(days=180):
        recommendations.append({
            'type': 'update_password',
            'title': 'تحديث كلمة المرور',
            'description': 'ننصح بتحديث كلمة المرور كل 6 أشهر',
            'priority': 'medium'
        })
    
    return recommendations
