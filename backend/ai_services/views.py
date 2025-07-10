from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import tempfile

from .models import AIWasteClassification, AIChatConversation, AIChatMessage
from .serializers import (
    AIWasteClassificationSerializer,
    AIChatConversationSerializer,
    AIChatConversationDetailSerializer,
    AIChatMessageSerializer,
    SendMessageSerializer,
    CreateConversationSerializer,
    ClassifyImageSerializer,
    UserFeedbackSerializer
)
from .services import WasteClassificationService, AIChatService, AIRecommendationService
from items.models import Item

class AIWasteClassificationView(generics.ListAPIView):
    """عرض تصنيفات AI للمستخدم"""
    serializer_class = AIWasteClassificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AIWasteClassification.objects.filter(
            item__user=self.request.user
        ).order_by('-created_at')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def classify_waste_image(request):
    """تصنيف صورة المخلفات بالذكاء الاصطناعي"""
    serializer = ClassifyImageSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        image = serializer.validated_data['image']
        description = serializer.validated_data.get('description', '')
        
        # حفظ الصورة مؤقتاً
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            for chunk in image.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name
        
        # تصنيف الصورة
        classification_service = WasteClassificationService()
        result = classification_service.classify_waste_image(temp_path, description)
        
        # حذف الملف المؤقت
        os.unlink(temp_path)
        
        if result.get('success'):
            return Response({
                'success': True,
                'classification': {
                    'category': result['predicted_category'],
                    'category_ar': result['predicted_category_ar'],
                    'confidence': result['confidence_score'],
                    'confidence_level': result['confidence_level'],
                    'material_composition': result['material_composition'],
                    'recyclability_score': result['recyclability_score'],
                    'environmental_impact': result['environmental_impact'],
                    'price_range': result['suggested_price_range'],
                    'recycling_tips': result['recycling_tips'],
                    'safety_warnings': result['safety_warnings'],
                    'processing_time': result['processing_time']
                }
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'فشل في تصنيف الصورة')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def classify_item_image(request, item_id):
    """تصنيف صورة منتج موجود"""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    
    # التحقق من وجود صور للمنتج
    primary_image = item.images.filter(is_primary=True).first()
    if not primary_image:
        return Response({
            'success': False,
            'error': 'لا توجد صورة أساسية للمنتج'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # تصنيف الصورة
        classification_service = WasteClassificationService()
        image_url = request.build_absolute_uri(primary_image.image.url)
        result = classification_service.classify_waste_image(image_url, item.description)
        
        if result.get('success'):
            # حفظ النتيجة
            classification = classification_service.save_classification_result(
                item, image_url, result
            )
            
            serializer = AIWasteClassificationSerializer(classification)
            return Response({
                'success': True,
                'classification': serializer.data
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'فشل في تصنيف الصورة')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AIChatConversationListView(generics.ListAPIView):
    """قائمة محادثات AI للمستخدم"""
    serializer_class = AIChatConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AIChatConversation.objects.filter(
            user=self.request.user
        ).order_by('-updated_at')

class AIChatConversationDetailView(generics.RetrieveAPIView):
    """تفاصيل محادثة AI"""
    serializer_class = AIChatConversationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AIChatConversation.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_ai_conversation(request):
    """إنشاء محادثة AI جديدة"""
    serializer = CreateConversationSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        chat_service = AIChatService()
        conversation = chat_service.create_conversation(
            user=request.user,
            conversation_type=serializer.validated_data['conversation_type'],
            title=serializer.validated_data['title'],
            context_data=serializer.validated_data.get('context_data', {})
        )
        
        # إرسال رسالة أولى إذا كانت موجودة
        initial_message = serializer.validated_data.get('initial_message')
        if initial_message:
            chat_service.send_message(conversation, initial_message)
        
        # إرجاع تفاصيل المحادثة
        response_serializer = AIChatConversationDetailSerializer(conversation)
        return Response({
            'success': True,
            'conversation': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ في إنشاء المحادثة: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_ai_message(request, conversation_id):
    """إرسال رسالة في محادثة AI"""
    conversation = get_object_or_404(
        AIChatConversation, 
        id=conversation_id, 
        user=request.user
    )
    
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        chat_service = AIChatService()
        
        # معالجة المرفقات إذا كانت موجودة
        attachments = []
        if 'attachments' in request.FILES:
            for file in request.FILES.getlist('attachments'):
                # حفظ الملف وإضافة رابطه
                file_path = default_storage.save(f'ai_chat/{file.name}', ContentFile(file.read()))
                attachments.append({
                    'name': file.name,
                    'url': default_storage.url(file_path),
                    'type': file.content_type
                })
        
        # إرسال الرسالة
        ai_message = chat_service.send_message(
            conversation=conversation,
            user_message=serializer.validated_data['message'],
            attachments=attachments
        )
        
        # إرجاع آخر رسالتين (المستخدم + AI)
        recent_messages = conversation.messages.order_by('-created_at')[:2]
        messages_serializer = AIChatMessageSerializer(
            reversed(recent_messages), 
            many=True
        )
        
        return Response({
            'success': True,
            'messages': messages_serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ في إرسال الرسالة: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rate_ai_message(request, message_id):
    """تقييم رسالة AI"""
    message = get_object_or_404(
        AIChatMessage,
        id=message_id,
        conversation__user=request.user,
        message_type='ai'
    )
    
    rating = request.data.get('rating')
    is_helpful = request.data.get('is_helpful')
    
    if rating is not None:
        if not (1 <= int(rating) <= 5):
            return Response({
                'error': 'التقييم يجب أن يكون بين 1 و 5'
            }, status=status.HTTP_400_BAD_REQUEST)
        message.user_rating = int(rating)
    
    if is_helpful is not None:
        message.is_helpful = bool(is_helpful)
    
    message.save()
    
    return Response({
        'success': True,
        'message': 'تم حفظ التقييم بنجاح'
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_classification_feedback(request):
    """تقديم ملاحظات على تصنيف AI"""
    serializer = UserFeedbackSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        classification = get_object_or_404(
            AIWasteClassification,
            id=serializer.validated_data['classification_id'],
            item__user=request.user
        )
        
        # حفظ الملاحظات
        classification.user_feedback = serializer.validated_data['feedback']
        if serializer.validated_data.get('correct_category'):
            classification.manual_correction = serializer.validated_data['correct_category']
        
        classification.save()
        
        # حفظ بيانات التدريب للتحسين المستقبلي
        from .models import AITrainingData
        AITrainingData.objects.create(
            data_type='image_classification',
            input_data={
                'image_url': classification.image_url,
                'description': classification.item.description
            },
            expected_output={
                'category': serializer.validated_data.get('correct_category', classification.predicted_category),
                'feedback': serializer.validated_data['feedback']
            },
            source='user_feedback',
            item=classification.item
        )
        
        return Response({
            'success': True,
            'message': 'شكراً لك! ملاحظاتك ستساعد في تحسين دقة النظام'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_ai_recommendations(request):
    """الحصول على توصيات AI للمستخدم"""
    try:
        recommendation_service = AIRecommendationService()
        recommendations = recommendation_service.get_item_recommendations(
            user=request.user,
            limit=int(request.GET.get('limit', 5))
        )
        
        return Response({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'حدث خطأ في جلب التوصيات: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_ai_stats(request):
    """إحصائيات AI للمستخدم"""
    user = request.user
    
    # إحصائيات التصنيف
    classifications = AIWasteClassification.objects.filter(item__user=user)
    total_classifications = classifications.count()
    successful_classifications = classifications.filter(status='completed').count()
    high_confidence_classifications = classifications.filter(confidence_level__in=['high', 'very_high']).count()
    
    # إحصائيات المحادثات
    conversations = AIChatConversation.objects.filter(user=user)
    total_conversations = conversations.count()
    active_conversations = conversations.filter(is_active=True).count()
    total_messages = AIChatMessage.objects.filter(conversation__user=user).count()
    
    return Response({
        'classification_stats': {
            'total': total_classifications,
            'successful': successful_classifications,
            'high_confidence': high_confidence_classifications,
            'success_rate': (successful_classifications / total_classifications * 100) if total_classifications > 0 else 0
        },
        'chat_stats': {
            'total_conversations': total_conversations,
            'active_conversations': active_conversations,
            'total_messages': total_messages,
            'avg_messages_per_conversation': (total_messages / total_conversations) if total_conversations > 0 else 0
        }
    })
