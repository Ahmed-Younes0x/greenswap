from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging
from .models import AIWasteClassification, AIModelPerformance, AIChatMessage
from .services import WasteClassificationService

logger = logging.getLogger(__name__)

@shared_task
def process_pending_classifications():
    """معالجة التصنيفات المعلقة"""
    pending_classifications = AIWasteClassification.objects.filter(
        status='pending',
        created_at__gte=timezone.now() - timedelta(hours=24)
    )
    
    classification_service = WasteClassificationService()
    processed_count = 0
    
    for classification in pending_classifications:
        try:
            result = classification_service.classify_waste_image(
                classification.image_url,
                classification.item.description
            )
            
            if result.get('success'):
                # تحديث التصنيف
                classification.predicted_category = result['predicted_category']
                classification.predicted_category_ar = result['predicted_category_ar']
                classification.confidence_score = result['confidence_score']
                classification.confidence_level = result['confidence_level']
                classification.material_composition = result['material_composition']
                classification.recyclability_score = result['recyclability_score']
                classification.environmental_impact = result['environmental_impact']
                classification.suggested_price_range = result['suggested_price_range']
                classification.recycling_tips = result['recycling_tips']
                classification.safety_warnings = result['safety_warnings']
                classification.status = 'completed'
                classification.processing_time = result['processing_time']
                classification.save()
                
                processed_count += 1
            else:
                classification.status = 'failed'
                classification.error_message = result.get('error', 'خطأ غير معروف')
                classification.save()
                
        except Exception as e:
            logger.error(f"خطأ في معالجة التصنيف {classification.id}: {str(e)}")
            classification.status = 'failed'
            classification.error_message = str(e)
            classification.save()
    
    logger.info(f"تم معالجة {processed_count} تصنيف من أصل {pending_classifications.count()}")
    return processed_count

@shared_task
def update_ai_performance_stats():
    """تحديث إحصائيات أداء AI"""
    today = timezone.now().date()
    
    # إحصائيات التصنيف
    classifications_today = AIWasteClassification.objects.filter(
        created_at__date=today
    )
    
    total_classifications = classifications_today.count()
    successful_classifications = classifications_today.filter(status='completed').count()
    failed_classifications = classifications_today.filter(status='failed').count()
    
    if total_classifications > 0:
        # حساب متوسط وقت الاستجابة
        completed_classifications = classifications_today.filter(
            status='completed',
            processing_time__isnull=False
        )
        
        if completed_classifications.exists():
            avg_response_time = completed_classifications.aggregate(
                avg_time=models.Avg('processing_time')
            )['avg_time']
            
            min_response_time = completed_classifications.aggregate(
                min_time=models.Min('processing_time')
            )['min_time']
            
            max_response_time = completed_classifications.aggregate(
                max_time=models.Max('processing_time')
            )['max_time']
        else:
            avg_response_time = min_response_time = max_response_time = 0
        
        # حساب دقة النموذج بناءً على ملاحظات المستخدمين
        feedback_classifications = classifications_today.filter(
            user_feedback__isnull=False
        )
        
        if feedback_classifications.exists():
            correct_feedback = feedback_classifications.filter(user_feedback='correct').count()
            accuracy_score = correct_feedback / feedback_classifications.count()
        else:
            accuracy_score = 0.95  # افتراضي
        
        # حفظ أو تحديث الإحصائيات
        performance, created = AIModelPerformance.objects.get_or_create(
            model_name='gpt-4-vision-preview',
            model_version='1.0',
            date=today,
            defaults={
                'total_requests': total_classifications,
                'successful_requests': successful_classifications,
                'failed_requests': failed_classifications,
                'avg_response_time': avg_response_time,
                'min_response_time': min_response_time,
                'max_response_time': max_response_time,
                'accuracy_score': accuracy_score,
            }
        )
        
        if not created:
            performance.total_requests = total_classifications
            performance.successful_requests = successful_classifications
            performance.failed_requests = failed_classifications
            performance.avg_response_time = avg_response_time
            performance.min_response_time = min_response_time
            performance.max_response_time = max_response_time
            performance.accuracy_score = accuracy_score
            performance.save()
    
    # إحصائيات المحادثات
    chat_messages_today = AIChatMessage.objects.filter(
        created_at__date=today,
        message_type='ai'
    )
    
    total_chat_tokens = chat_messages_today.aggregate(
        total_tokens=models.Sum('tokens_used')
    )['total_tokens'] or 0
    
    # تحديث إحصائيات المحادثة
    chat_performance, created = AIModelPerformance.objects.get_or_create(
        model_name='gpt-4-turbo-preview',
        model_version='1.0',
        date=today,
        defaults={
            'total_requests': chat_messages_today.count(),
            'successful_requests': chat_messages_today.count(),
            'total_tokens_used': total_chat_tokens,
        }
    )
    
    if not created:
        chat_performance.total_requests = chat_messages_today.count()
        chat_performance.successful_requests = chat_messages_today.count()
        chat_performance.total_tokens_used = total_chat_tokens
        chat_performance.save()
    
    logger.info(f"تم تحديث إحصائيات الأداء لتاريخ {today}")

@shared_task
def cleanup_old_ai_data():
    """تنظيف البيانات القديمة"""
    # حذف التصنيفات الفاشلة القديمة (أكثر من 30 يوم)
    old_failed_classifications = AIWasteClassification.objects.filter(
        status='failed',
        created_at__lt=timezone.now() - timedelta(days=30)
    )
    deleted_count = old_failed_classifications.count()
    old_failed_classifications.delete()
    
    # حذف المحادثات غير النشطة القديمة (أكثر من 90 يوم)
    old_conversations = AIChatConversation.objects.filter(
        is_active=False,
        updated_at__lt=timezone.now() - timedelta(days=90)
    )
    deleted_conversations = old_conversations.count()
    old_conversations.delete()
    
    logger.info(f"تم حذف {deleted_count} تصنيف فاشل و {deleted_conversations} محادثة قديمة")

@shared_task
def retrain_ai_model():
    """إعادة تدريب النموذج بناءً على البيانات الجديدة"""
    # هذه مهمة معقدة تحتاج تطبيق مخصص
    # يمكن تطويرها لاحقاً لتحسين دقة النموذج
    logger.info("بدء عملية إعادة تدريب النموذج...")
    
    # جمع بيانات التدريب الجديدة
    from .models import AITrainingData
    new_training_data = AITrainingData.objects.filter(
        is_verified=True,
        created_at__gte=timezone.now() - timedelta(days=7)
    )
    
    if new_training_data.count() >= 100:  # حد أدنى للبيانات
        # تطبيق خوارزمية التدريب
        # هذا يحتاج تطبيق مخصص حسب نوع النموذج
        logger.info(f"تم العثور على {new_training_data.count()} عينة تدريب جديدة")
        # TODO: تطبيق التدريب الفعلي
    else:
        logger.info("لا توجد بيانات تدريب كافية لإعادة التدريب")
