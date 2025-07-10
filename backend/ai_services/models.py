from django.db import models
from accounts.models import User
from items.models import Item
import json

class AIWasteClassification(models.Model):
    """نموذج تصنيف المخلفات بالذكاء الاصطناعي"""
    
    CONFIDENCE_LEVELS = [
        ('very_high', 'عالية جداً (95%+)'),
        ('high', 'عالية (85-94%)'),
        ('medium', 'متوسطة (70-84%)'),
        ('low', 'منخفضة (50-69%)'),
        ('very_low', 'منخفضة جداً (<50%)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
        ('reviewing', 'قيد المراجعة'),
    ]
    
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='ai_classification')
    image_url = models.URLField(max_length=500)
    predicted_category = models.CharField(max_length=100)
    predicted_category_ar = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVELS)
    
    # تفاصيل التصنيف
    material_composition = models.JSONField(default=dict)  # {"plastic": 0.8, "metal": 0.2}
    recyclability_score = models.FloatField(default=0.0)  # 0-1
    environmental_impact = models.CharField(max_length=20, default='medium')
    
    # معلومات إضافية من AI
    suggested_price_range = models.JSONField(default=dict)  # {"min": 10, "max": 50}
    recycling_tips = models.TextField(blank=True)
    safety_warnings = models.TextField(blank=True)
    
    # حالة المعالجة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processing_time = models.FloatField(null=True, blank=True)  # بالثواني
    error_message = models.TextField(blank=True)
    
    # تحسين النموذج
    user_feedback = models.CharField(max_length=20, blank=True)  # correct/incorrect
    manual_correction = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "تصنيف AI للمخلفات"
        verbose_name_plural = "تصنيفات AI للمخلفات"
    
    def __str__(self):
        return f"AI Classification: {self.item.title} - {self.predicted_category_ar}"
    
    @property
    def is_high_confidence(self):
        return self.confidence_score >= 0.85
    
    @property
    def material_breakdown(self):
        """تفصيل المواد المكونة"""
        return json.dumps(self.material_composition, ensure_ascii=False)

class AIChatConversation(models.Model):
    """محادثات الذكاء الاصطناعي"""
    
    CONVERSATION_TYPES = [
        ('waste_inquiry', 'استفسار عن المخلفات'),
        ('recycling_advice', 'نصائح إعادة التدوير'),
        ('price_estimation', 'تقدير الأسعار'),
        ('general_support', 'دعم عام'),
        ('item_recommendation', 'توصيات المنتجات'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    conversation_type = models.CharField(max_length=30, choices=CONVERSATION_TYPES)
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    # إعدادات AI
    ai_model_used = models.CharField(max_length=50, default='gpt-4')
    context_data = models.JSONField(default=dict)  # سياق المحادثة
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "محادثة AI"
        verbose_name_plural = "محادثات AI"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"AI Chat: {self.user.username} - {self.title}"

class AIChatMessage(models.Model):
    """رسائل محادثات الذكاء الاصطناعي"""
    
    MESSAGE_TYPES = [
        ('user', 'مستخدم'),
        ('ai', 'ذكاء اصطناعي'),
        ('system', 'نظام'),
    ]
    
    conversation = models.ForeignKey(AIChatConversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    
    # معلومات AI
    ai_confidence = models.FloatField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    
    # مرفقات
    attachments = models.JSONField(default=list)  # صور، ملفات
    
    # تفاعل المستخدم
    user_rating = models.IntegerField(null=True, blank=True)  # 1-5
    is_helpful = models.BooleanField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "رسالة AI"
        verbose_name_plural = "رسائل AI"
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}..."

class AIModelPerformance(models.Model):
    """أداء نماذج الذكاء الاصطناعي"""
    
    model_name = models.CharField(max_length=50)
    model_version = models.CharField(max_length=20)
    
    # إحصائيات الأداء
    total_requests = models.IntegerField(default=0)
    successful_requests = models.IntegerField(default=0)
    failed_requests = models.IntegerField(default=0)
    
    # أوقات الاستجابة
    avg_response_time = models.FloatField(default=0.0)
    min_response_time = models.FloatField(default=0.0)
    max_response_time = models.FloatField(default=0.0)
    
    # دقة النموذج
    accuracy_score = models.FloatField(default=0.0)
    precision_score = models.FloatField(default=0.0)
    recall_score = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    
    # استخدام الموارد
    total_tokens_used = models.BigIntegerField(default=0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "أداء نموذج AI"
        verbose_name_plural = "أداء نماذج AI"
        unique_together = ['model_name', 'model_version', 'date']
    
    def __str__(self):
        return f"{self.model_name} v{self.model_version} - {self.date}"

class AITrainingData(models.Model):
    """بيانات تدريب الذكاء الاصطناعي"""
    
    DATA_TYPES = [
        ('image_classification', 'تصنيف الصور'),
        ('text_classification', 'تصنيف النصوص'),
        ('chat_response', 'ردود المحادثة'),
        ('price_prediction', 'توقع الأسعار'),
    ]
    
    data_type = models.CharField(max_length=30, choices=DATA_TYPES)
    input_data = models.JSONField()  # البيانات المدخلة
    expected_output = models.JSONField()  # النتيجة المتوقعة
    actual_output = models.JSONField(null=True, blank=True)  # النتيجة الفعلية
    
    # معلومات الجودة
    is_verified = models.BooleanField(default=False)
    quality_score = models.FloatField(default=0.0)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # معلومات المصدر
    source = models.CharField(max_length=100)  # user_feedback, manual_entry, etc.
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "بيانات تدريب AI"
        verbose_name_plural = "بيانات تدريب AI"
    
    def __str__(self):
        return f"Training Data: {self.get_data_type_display()} - {self.created_at.date()}"
