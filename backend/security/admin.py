from django.contrib import admin
from .models import (
    APIKey, TwoFactorAuth, SecurityLog, 
    RateLimitRecord, FileUploadLog, OAuth2Application
)

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'rate_limit', 'usage_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username', 'user__email']
    readonly_fields = ['key', 'usage_count', 'last_used']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['user']
        return self.readonly_fields

@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_enabled', 'created_at', 'last_used']
    list_filter = ['is_enabled', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['secret_key', 'backup_codes']

@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'severity', 'ip_address', 'timestamp', 'is_resolved']
    list_filter = ['event_type', 'severity', 'is_resolved', 'timestamp']
    search_fields = ['user__username', 'ip_address', 'user_agent']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # منع إضافة سجلات يدوياً

@admin.register(RateLimitRecord)
class RateLimitRecordAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'endpoint', 'request_count', 'window_start', 'is_blocked']
    list_filter = ['is_blocked', 'window_start']
    search_fields = ['identifier', 'endpoint']

@admin.register(FileUploadLog)
class FileUploadLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'filename', 'file_size', 'file_type', 'is_safe', 'uploaded_at']
    list_filter = ['is_safe', 'file_type', 'uploaded_at']
    search_fields = ['user__username', 'filename', 'ip_address']
    readonly_fields = ['file_hash', 'uploaded_at']

@admin.register(OAuth2Application)
class OAuth2ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_id', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'client_id', 'created_by__username']
    readonly_fields = ['client_id', 'client_secret']
