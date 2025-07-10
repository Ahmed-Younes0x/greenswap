from django.contrib import admin
from .models import (
    AIWasteClassification, 
    AIChatConversation, 
    AIChatMessage,
    AIModelPerformance,
    AITrainingData
)

@admin.register(AIWasteClassification)
class AIWasteClassificationAdmin(admin.ModelAdmin):
    list_display = [
        'item', 'predicted_category_ar', 'confidence_score', 
        'confidence_level', 'status', 'created_at'
    ]
    list_filter = [
        'predicted_category', 'confidence_level', 'status', 
        'environmental_impact', 'created_at'
    ]
    search_fields = ['item__title', 'predicted_category', 'predicted_category_ar']
    readonly_fields = ['processing_time', 'created_at', 'updated_at']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('item', 'image_url', 'status')
        }),
        ('نتائج التصنيف', {
            'fields': (
                'predicted_category', 'predicted_category_ar',
                'confidence_score', 'confidence_level'
            )
        }),
        ('تحليل مفصل', {
            'fields': (
                'material_composition', 'recyclability_score',
                'environmental_impact', 'suggested_price_range'
            )
        }),
        ('نصائح وتحذيرات', {
            'fields': ('recycling_tips', 'safety_warnings')
        }),
        ('ملاحظات المستخدم', {
            'fields': ('user_feedback', 'manual_correction')
        }),
        ('معلومات تقنية', {
            'fields': ('processing_time', 'error_message', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

class AIChatMessageInline(admin.TabularInline):
    model = AIChatMessage
    extra = 0
    readonly_fields = ['created_at', 'processing_time', 'tokens_used']
    fields = ['message_type', 'content', 'ai_confidence', 'user_rating', 'created_at']

@admin.register(AIChatConversation)
class AIChatConversationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'user', 'conversation_type', 'is_active', 
        'messages_count', 'created_at'
    ]
    list_filter = ['conversation_type', 'is_active', 'created_at']
    search_fields = ['title', 'user__username', 'user__email']
    inlines = [AIChatMessageInline]
    
    def messages_count(self, obj):
        return obj.messages.count()
    messages_count.short_description = 'عدد الرسائل'

@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        'conversation', 'message_type', 'content_preview', 
        'ai_confidence', 'user_rating', 'created_at'
    ]
    list_filter = ['message_type', 'user_rating', 'is_helpful', 'created_at']
    search_fields = ['content', 'conversation__title']
    readonly_fields = ['processing_time', 'tokens_used', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'محتوى الرسالة'

@admin.register(AIModelPerformance)
class AIModelPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        'model_name', 'model_version', 'date', 'total_requests',
        'success_rate', 'avg_response_time', 'accuracy_score'
    ]
    list_filter = ['model_name', 'date']
    readonly_fields = ['created_at']
    
    def success_rate(self, obj):
        if obj.total_requests > 0:
            return f"{(obj.successful_requests / obj.total_requests * 100):.1f}%"
        return "0%"
    success_rate.short_description = 'معدل النجاح'

@admin.register(AITrainingData)
class AITrainingDataAdmin(admin.ModelAdmin):
    list_display = [
        'data_type', 'source', 'is_verified', 'quality_score',
        'verified_by', 'created_at'
    ]
    list_filter = ['data_type', 'is_verifie', 'source', 'created_at']
    search_fields = ['source', 'item__title']
    readonly_fields = ['created_at']
