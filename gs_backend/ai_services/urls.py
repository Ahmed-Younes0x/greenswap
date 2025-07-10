from django.urls import path
from . import views

urlpatterns = [
    # تصنيف المخلفات
    path('classify/image/', views.classify_waste_image, name='classify_waste_image'),
    path('classify/item/<int:item_id>/', views.classify_item_image, name='classify_item_image'),
    path('classifications/', views.AIWasteClassificationView.as_view(), name='ai_classifications'),
    path('feedback/', views.submit_classification_feedback, name='classification_feedback'),
    
    # المحادثات الذكية
    path('chat/conversations/', views.AIChatConversationListView.as_view(), name='ai_conversations'),
    path('chat/conversations/create/', views.create_ai_conversation, name='create_ai_conversation'),
    path('chat/conversations/<int:pk>/', views.AIChatConversationDetailView.as_view(), name='ai_conversation_detail'),
    path('chat/conversations/<int:conversation_id>/send/', views.send_ai_message, name='send_ai_message'),
    path('chat/messages/<int:message_id>/rate/', views.rate_ai_message, name='rate_ai_message'),
    
    # التوصيات والإحصائيات
    path('recommendations/', views.get_ai_recommendations, name='ai_recommendations'),
    path('stats/', views.get_ai_stats, name='ai_stats'),
]
