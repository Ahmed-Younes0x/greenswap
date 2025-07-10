from django.urls import path, include
from . import views

app_name = 'security'

urlpatterns = [
    # API Keys
    path('api-keys/', views.APIKeyListCreateView.as_view(), name='api-keys'),
    path('api-keys/<int:pk>/', views.APIKeyDetailView.as_view(), name='api-key-detail'),
    
    # Two-Factor Authentication
    path('2fa/setup/', views.setup_2fa, name='setup-2fa'),
    path('2fa/enable/', views.enable_2fa, name='enable-2fa'),
    path('2fa/disable/', views.disable_2fa, name='disable-2fa'),
    path('2fa/status/', views.get_2fa_status, name='2fa-status'),
    path('2fa/verify-login/', views.verify_2fa_login, name='verify-2fa-login'),
    
    # Security Logs
    path('logs/', views.SecurityLogListView.as_view(), name='security-logs'),
    path('dashboard/', views.get_security_dashboard, name='security-dashboard'),
    
    # Password Management
    path('change-password/', views.change_password, name='change-password'),
]
