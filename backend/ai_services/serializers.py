from rest_framework import serializers
from .models import AIWasteClassification, AIChatConversation, AIChatMessage

class AIWasteClassificationSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(source='item.title', read_only=True)
    confidence_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = AIWasteClassification
        fields = [
            'id', 'item_title', 'predicted_category', 'predicted_category_ar',
            'confidence_score', 'confidence_percentage', 'confidence_level',
            'material_composition', 'recyclability_score', 'environmental_impact',
            'suggested_price_range', 'recycling_tips', 'safety_warnings',
            'status', 'processing_time', 'created_at'
        ]
    
    def get_confidence_percentage(self, obj):
        return f"{obj.confidence_score * 100:.1f}%"

class AIChatMessageSerializer(serializers.ModelSerializer):
    is_from_user = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()
    
    class Meta:
        model = AIChatMessage
        fields = [
            'id', 'message_type', 'content', 'is_from_user',
            'ai_confidence', 'processing_time', 'attachments',
            'user_rating', 'is_helpful', 'created_at', 'formatted_time'
        ]
    
    def get_is_from_user(self, obj):
        return obj.message_type == 'user'
    
    def get_formatted_time(self, obj):
        return obj.created_at.strftime('%H:%M')

class AIChatConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    conversation_type_display = serializers.CharField(source='get_conversation_type_display', read_only=True)
    
    class Meta:
        model = AIChatConversation
        fields = [
            'id', 'conversation_type', 'conversation_type_display', 'title',
            'is_active', 'last_message', 'messages_count', 'created_at', 'updated_at'
        ]
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'content': last_msg.content[:100] + '...' if len(last_msg.content) > 100 else last_msg.content,
                'message_type': last_msg.message_type,
                'created_at': last_msg.created_at
            }
        return None
    
    def get_messages_count(self, obj):
        return obj.messages.count()

class AIChatConversationDetailSerializer(serializers.ModelSerializer):
    messages = AIChatMessageSerializer(many=True, read_only=True)
    conversation_type_display = serializers.CharField(source='get_conversation_type_display', read_only=True)
    
    class Meta:
        model = AIChatConversation
        fields = [
            'id', 'conversation_type', 'conversation_type_display', 'title',
            'is_active', 'messages', 'created_at', 'updated_at'
        ]

class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True
    )

class CreateConversationSerializer(serializers.Serializer):
    conversation_type = serializers.ChoiceField(choices=AIChatConversation.CONVERSATION_TYPES)
    title = serializers.CharField(max_length=200)
    initial_message = serializers.CharField(max_length=2000, required=False)
    context_data = serializers.JSONField(required=False)

class ClassifyImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_image(self, value):
        # التحقق من حجم الصورة (أقل من 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("حجم الصورة يجب أن يكون أقل من 10 ميجابايت")
        
        # التحقق من نوع الملف
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("نوع الملف غير مدعوم. استخدم JPG أو PNG")
        
        return value

class UserFeedbackSerializer(serializers.Serializer):
    classification_id = serializers.IntegerField()
    feedback = serializers.ChoiceField(choices=['correct', 'incorrect'])
    correct_category = serializers.CharField(max_length=100, required=False)
    comments = serializers.CharField(max_length=500, required=False)
