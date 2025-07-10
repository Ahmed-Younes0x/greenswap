from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import secrets
import string

User = get_user_model()

class APIKey(models.Model):
    """نموذج مفاتيح API للمطورين الخارجيين"""
    name = models.CharField(max_length=100, verbose_name="اسم المفتاح")
    key = models.CharField(max_length=64, unique=True, verbose_name="المفتاح")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    permissions = models.JSONField(default=list, verbose_name="الصلاحيات")
    rate_limit = models.IntegerField(default=1000, verbose_name="حد الطلبات/ساعة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    last_used = models.DateTimeField(null=True, blank=True, verbose_name="آخر استخدام")
    usage_count = models.IntegerField(default=0, verbose_name="عدد الاستخدامات")
    
    class Meta:
        verbose_name = "مفتاح API"
        verbose_name_plural = "مفاتيح API"
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_key():
        """توليد مفتاح API آمن"""
        alphabet = string.ascii_letters + string.digits
        return 'gse_' + ''.join(secrets.choice(alphabet) for _ in range(60))
    
    def __str__(self):
        return f"{self.name} - {self.key[:20]}..."

class TwoFactorAuth(models.Model):
    """نموذج المصادقة الثنائية"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    secret_key = models.CharField(max_length=32, verbose_name="المفتاح السري")
    is_enabled = models.BooleanField(default=False, verbose_name="مفعل")
    backup_codes = models.JSONField(default=list, verbose_name="رموز النسخ الاحتياطي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    last_used = models.DateTimeField(null=True, blank=True, verbose_name="آخر استخدام")
    
    class Meta:
        verbose_name = "المصادقة الثنائية"
        verbose_name_plural = "المصادقة الثنائية"
    
    def generate_backup_codes(self):
        """توليد رموز النسخ الاحتياطي"""
        codes = []
        for _ in range(10):
            code = ''.join(secrets.choice(string.digits) for _ in range(8))
            codes.append(code)
        self.backup_codes = codes
        return codes
    
    def __str__(self):
        return f"2FA - {self.user.username}"

class SecurityLog(models.Model):
    """سجل الأمان والأنشطة المشبوهة"""
    SEVERITY_CHOICES = [
        ('low', 'منخفض'),
        ('medium', 'متوسط'),
        ('high', 'عالي'),
        ('critical', 'حرج'),
    ]
    
    EVENT_TYPES = [
        ('login_attempt', 'محاولة تسجيل دخول'),
        ('failed_login', 'فشل تسجيل دخول'),
        ('rate_limit_exceeded', 'تجاوز حد الطلبات'),
        ('suspicious_activity', 'نشاط مشبوه'),
        ('file_upload', 'رفع ملف'),
        ('api_access', 'وصول API'),
        ('data_breach_attempt', 'محاولة اختراق بيانات'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المستخدم")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name="نوع الحدث")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, verbose_name="الخطورة")
    ip_address = models.GenericIPAddressField(verbose_name="عنوان IP")
    user_agent = models.TextField(verbose_name="معلومات المتصفح")
    details = models.JSONField(default=dict, verbose_name="التفاصيل")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="الوقت")
    is_resolved = models.BooleanField(default=False, verbose_name="تم الحل")
    
    class Meta:
        verbose_name = "سجل الأمان"
        verbose_name_plural = "سجلات الأمان"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.event_type} - {self.severity} - {self.timestamp}"

class RateLimitRecord(models.Model):
    """سجل حدود الطلبات"""
    identifier = models.CharField(max_length=100, verbose_name="المعرف")  # IP أو User ID
    endpoint = models.CharField(max_length=200, verbose_name="نقطة النهاية")
    request_count = models.IntegerField(default=0, verbose_name="عدد الطلبات")
    window_start = models.DateTimeField(verbose_name="بداية النافزة الزمنية")
    is_blocked = models.BooleanField(default=False, verbose_name="محظور")
    
    class Meta:
        verbose_name = "سجل حدود الطلبات"
        verbose_name_plural = "سجلات حدود الطلبات"
        unique_together = ['identifier', 'endpoint', 'window_start']
    
    def __str__(self):
        return f"{self.identifier} - {self.endpoint} - {self.request_count}"

class FileUploadLog(models.Model):
    """سجل رفع الملفات للمراقبة الأمنية"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم")
    filename = models.CharField(max_length=255, verbose_name="اسم الملف")
    file_size = models.BigIntegerField(verbose_name="حجم الملف")
    file_type = models.CharField(max_length=100, verbose_name="نوع الملف")
    file_hash = models.CharField(max_length=64, verbose_name="هاش الملف")
    ip_address = models.GenericIPAddressField(verbose_name="عنوان IP")
    is_safe = models.BooleanField(default=True, verbose_name="آمن")
    scan_results = models.JSONField(default=dict, verbose_name="نتائج الفحص")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الرفع")
    
    class Meta:
        verbose_name = "سجل رفع الملفات"
        verbose_name_plural = "سجلات رفع الملفات"
    
    def __str__(self):
        return f"{self.filename} - {self.user.username}"

class OAuth2Application(models.Model):
    """تطبيقات OAuth2 المسجلة"""
    name = models.CharField(max_length=100, verbose_name="اسم التطبيق")
    client_id = models.CharField(max_length=100, unique=True, verbose_name="معرف العميل")
    client_secret = models.CharField(max_length=255, verbose_name="سر العميل")
    redirect_uris = models.TextField(verbose_name="روابط إعادة التوجيه")
    scopes = models.JSONField(default=list, verbose_name="النطاقات")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="أنشأ بواسطة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    class Meta:
        verbose_name = "تطبيق OAuth2"
        verbose_name_plural = "تطبيقات OAuth2"
    
    def save(self, *args, **kwargs):
        if not self.client_id:
            self.client_id = secrets.token_urlsafe(32)
        if not self.client_secret:
            self.client_secret = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
