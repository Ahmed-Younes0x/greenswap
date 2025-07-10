from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import APIKey, TwoFactorAuth, SecurityLog
from .validators import SecureInputValidator

class APIKeySerializer(serializers.ModelSerializer):
    """سيريالايزر مفاتيح API"""
    key = serializers.CharField(read_only=True)
    
    class Meta:
        model = APIKey
        fields = ['id', 'name', 'key', 'permissions', 'rate_limit', 
                 'is_active', 'created_at', 'last_used', 'usage_count']
        read_only_fields = ['key', 'created_at', 'last_used', 'usage_count']
    
    def validate_name(self, value):
        return SecureInputValidator.validate_input(value, 'name')
    
    def validate_permissions(self, value):
        allowed_permissions = [
            'read_items', 'create_items', 'update_items', 'delete_items',
            'read_users', 'read_orders', 'create_orders'
        ]
        
        for perm in value:
            if perm not in allowed_permissions:
                raise serializers.ValidationError(f'صلاحية غير مسموحة: {perm}')
        
        return value

class TwoFactorSetupSerializer(serializers.Serializer):
    """سيريالايزر إعداد المصادقة الثنائية"""
    otp_code = serializers.CharField(max_length=6, min_length=6)
    
    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('كود OTP يجب أن يحتوي على أرقام فقط')
        return value

class SecurityLogSerializer(serializers.ModelSerializer):
    """سيريالايزر سجلات الأمان"""
    class Meta:
        model = SecurityLog
        fields = ['id', 'event_type', 'severity', 'ip_address', 
                 'timestamp', 'details', 'is_resolved']

class ChangePasswordSerializer(serializers.Serializer):
    """سيريالايزر تغيير كلمة المرور"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("كلمات المرور الجديدة غير متطابقة")
        
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError("كلمة المرور الجديدة يجب أن تكون مختلفة عن القديمة")
        
        return attrs

class SecureFileUploadSerializer(serializers.Serializer):
    """سيريالايزر رفع الملفات الآمن"""
    file = serializers.FileField()
    description = serializers.CharField(max_length=500, required=False)
    
    def validate_file(self, value):
        from .validators import FileUploadValidator
        return FileUploadValidator.validate_file(value, ['images'])
    
    def validate_description(self, value):
        return SecureInputValidator.validate_input(value, 'description')

class OAuth2ApplicationSerializer(serializers.ModelSerializer):
    """سيريالايزر تطبيقات OAuth2"""
    client_secret = serializers.CharField(write_only=True)
    
    class Meta:
        model = OAuth2Application
        fields = ['id', 'name', 'client_id', 'client_secret', 
                 'redirect_uris', 'scopes', 'is_active', 'created_at']
        read_only_fields = ['client_id', 'created_at']
    
    def validate_name(self, value):
        return SecureInputValidator.validate_input(value, 'application_name')
    
    def validate_redirect_uris(self, value):
        import re
        uris = value.split('\n')
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        for uri in uris:
            uri = uri.strip()
            if uri and not url_pattern.match(uri):
                raise serializers.ValidationError(f'رابط غير صحيح: {uri}')
        
        return value
