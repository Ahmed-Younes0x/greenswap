from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/items/', include('items.urls')),
    # path('api/orders/', include('orders.urls')),
    # path('api/chat/', include('chat.urls')),
    # path('api/notifications/', include('notifications.urls')),
    # path('api/reviews/', include('reviews.urls')),
    # path('api/admin-panel/', include('admin_panel.urls')),
    path('api/ai/', include('ai_services.urls')),  # إضافة مسارات AI
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
