from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid

User = get_user_model()

class AnalyticsEvent(models.Model):
    """تتبع الأحداث والتفاعلات"""
    EVENT_TYPES = [
        ('page_view', 'مشاهدة صفحة'),
        ('click', 'نقرة'),
        ('form_submit', 'إرسال نموذج'),
        ('search', 'بحث'),
        ('item_view', 'مشاهدة عنصر'),
        ('item_share', 'مشاركة عنصر'),
        ('user_register', 'تسجيل مستخدم'),
        ('user_login', 'تسجيل دخول'),
        ('order_create', 'إنشاء طلب'),
        ('chat_message', 'رسالة محادثة'),
        ('ai_interaction', 'تفاعل مع AI'),
        ('custom', 'حدث مخصص'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    # معلومات الحدث
    properties = models.JSONField(default=dict, blank=True)
    page_url = models.URLField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    
    # معلومات المتصفح والجهاز
    user_agent = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=50, null=True, blank=True)
    
    # معلومات الموقع
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    
    # ربط بكائن آخر
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics_events'
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

class UserSession(models.Model):
    """جلسات المستخدمين"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, unique=True)
    
    # معلومات الجلسة
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    page_views = models.PositiveIntegerField(default=0)
    
    # معلومات الجهاز
    device_info = models.JSONField(default=dict, blank=True)
    location_info = models.JSONField(default=dict, blank=True)
    
    # إحصائيات الجلسة
    bounce_rate = models.FloatField(null=True, blank=True)
    conversion = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_sessions'
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['start_time']),
        ]

class ABTest(models.Model):
    """اختبارات A/B"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    # إعدادات الاختبار
    variants = models.JSONField(default=list)  # ['A', 'B', 'C']
    traffic_allocation = models.JSONField(default=dict)  # {'A': 50, 'B': 50}
    
    # حالة الاختبار
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # معايير النجاح
    success_metric = models.CharField(max_length=100)
    target_value = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ab_tests'

class ABTestParticipant(models.Model):
    """مشاركين في اختبارات A/B"""
    test = models.ForeignKey(ABTest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    variant = models.CharField(max_length=50)
    assigned_at = models.DateTimeField(auto_now_add=True)
    converted = models.BooleanField(default=False)
    conversion_value = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'ab_test_participants'
        unique_together = ['test', 'user', 'session_id']

class PerformanceMetric(models.Model):
    """مقاييس الأداء"""
    METRIC_TYPES = [
        ('page_load_time', 'وقت تحميل الصفحة'),
        ('api_response_time', 'وقت استجابة API'),
        ('database_query_time', 'وقت استعلام قاعدة البيانات'),
        ('cache_hit_rate', 'معدل نجاح الكاش'),
        ('error_rate', 'معدل الأخطاء'),
        ('memory_usage', 'استخدام الذاكرة'),
        ('cpu_usage', 'استخدام المعالج'),
        ('custom', 'مقياس مخصص'),
    ]
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    metric_name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=20, default='ms')
    
    # معلومات إضافية
    tags = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'performance_metrics'
        indexes = [
            models.Index(fields=['metric_type', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

class ErrorLog(models.Model):
    """سجل الأخطاء"""
    ERROR_LEVELS = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(max_length=20, choices=ERROR_LEVELS)
    message = models.TextField()
    
    # معلومات الخطأ
    exception_type = models.CharField(max_length=100, null=True, blank=True)
    stack_trace = models.TextField(null=True, blank=True)
    file_path = models.CharField(max_length=500, null=True, blank=True)
    line_number = models.PositiveIntegerField(null=True, blank=True)
    
    # معلومات السياق
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    request_url = models.URLField(null=True, blank=True)
    request_method = models.CharField(max_length=10, null=True, blank=True)
    
    # معلومات البيئة
    environment = models.CharField(max_length=50, default='production')
    server_name = models.CharField(max_length=100, null=True, blank=True)
    
    # معلومات إضافية
    extra_data = models.JSONField(default=dict, blank=True)
    
    # حالة الخطأ
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_errors')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'error_logs'
        indexes = [
            models.Index(fields=['level', 'timestamp']),
            models.Index(fields=['is_resolved', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
