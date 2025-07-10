import pyotp
import qrcode
import io
import base64
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey, TwoFactorAuth, SecurityLog
from .utils import get_client_ip

class APIKeyAuthentication(BaseAuthentication):
    """مصادقة مفاتيح API"""
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None
        
        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
            
            # تحديث آخر استخدام
            key_obj.last_used = timezone.now()
            key_obj.usage_count += 1
            key_obj.save(update_fields=['last_used', 'usage_count'])
            
            # فحص حدود الاستخدام
            if self.is_rate_limited(key_obj):
                raise AuthenticationFailed('تم تجاوز حد استخدام API key')
            
            # تسجيل الوصول
            SecurityLog.objects.create(
                user=key_obj.user,
                event_type='api_access',
                severity='low',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'api_key_name': key_obj.name}
            )
            
            return (key_obj.user, key_obj)
            
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('مفتاح API غير صحيح')
    
    def is_rate_limited(self, api_key):
        """فحص حدود الاستخدام لمفتاح API"""
        cache_key = f"api_rate_limit_{api_key.id}"
        current_hour = timezone.now().hour
        
        usage_data = cache.get(cache_key, {'hour': current_hour, 'count': 0})
        
        if usage_data['hour'] != current_hour:
            usage_data = {'hour': current_hour, 'count': 0}
        
        if usage_data['count'] >= api_key.rate_limit:
            return True
        
        usage_data['count'] += 1
        cache.set(cache_key, usage_data, 3600)  # ساعة واحدة
        return False

class TwoFactorAuthBackend(BaseBackend):
    """نظام المصادقة الثنائية"""
    
    def authenticate(self, request, username=None, password=None, otp_code=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            
            # التحقق من كلمة المرور أولاً
            if not user.check_password(password):
                return None
            
            # التحقق من المصادقة الثنائية إذا كانت مفعلة
            try:
                two_fa = TwoFactorAuth.objects.get(user=user, is_enabled=True)
                
                if not otp_code:
                    # المصادقة الثنائية مطلوبة لكن لم يتم تقديم الكود
                    return None
                
                if not self.verify_otp(two_fa, otp_code):
                    # كود OTP غير صحيح
                    SecurityLog.objects.create(
                        user=user,
                        event_type='failed_login',
                        severity='medium',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        details={'reason': 'invalid_2fa_code'}
                    )
                    return None
                
                # تحديث آخر استخدام للمصادقة الثنائية
                two_fa.last_used = timezone.now()
                two_fa.save(update_fields=['last_used'])
                
            except TwoFactorAuth.DoesNotExist:
                # المصادقة الثنائية غير مفعلة
                pass
            
            # تسجيل نجح تسجيل الدخول
            SecurityLog.objects.create(
                user=user,
                event_type='login_attempt',
                severity='low',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'success': True}
            )
            
            return user
            
        except User.DoesNotExist:
            return None
    
    def verify_otp(self, two_fa, otp_code):
        """التحقق من كود OTP"""
        totp = pyotp.TOTP(two_fa.secret_key)
        
        # التحقق من الكود الحالي
        if totp.verify(otp_code):
            return True
        
        # التحقق من رموز النسخ الاحتياطي
        if otp_code in two_fa.backup_codes:
            # إزالة الرمز المستخدم
            backup_codes = two_fa.backup_codes.copy()
            backup_codes.remove(otp_code)
            two_fa.backup_codes = backup_codes
            two_fa.save(update_fields=['backup_codes'])
            return True
        
        return False
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class TwoFactorAuthService:
    """خدمة المصادقة الثنائية"""
    
    @staticmethod
    def setup_2fa(user):
        """إعداد المصادقة الثنائية للمستخدم"""
        secret_key = pyotp.random_base32()
        
        two_fa, created = TwoFactorAuth.objects.get_or_create(
            user=user,
            defaults={'secret_key': secret_key}
        )
        
        if not created:
            two_fa.secret_key = secret_key
            two_fa.save()
        
        # توليد رموز النسخ الاحتياطي
        backup_codes = two_fa.generate_backup_codes()
        two_fa.save()
        
        # إنشاء QR code
        totp = pyotp.TOTP(secret_key)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="GreenSwap Egypt"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_code_data = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'secret_key': secret_key,
            'qr_code': f"data:image/png;base64,{qr_code_data}",
            'backup_codes': backup_codes
        }
    
    @staticmethod
    def enable_2fa(user, otp_code):
        """تفعيل المصادقة الثنائية"""
        try:
            two_fa = TwoFactorAuth.objects.get(user=user)
            totp = pyotp.TOTP(two_fa.secret_key)
            
            if totp.verify(otp_code):
                two_fa.is_enabled = True
                two_fa.save()
                return True
            return False
            
        except TwoFactorAuth.DoesNotExist:
            return False
    
    @staticmethod
    def disable_2fa(user, password):
        """إلغاء تفعيل المصادقة الثنائية"""
        if user.check_password(password):
            try:
                two_fa = TwoFactorAuth.objects.get(user=user)
                two_fa.is_enabled = False
                two_fa.save()
                return True
            except TwoFactorAuth.DoesNotExist:
                pass
        return False
