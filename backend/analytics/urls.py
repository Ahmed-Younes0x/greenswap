from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, ABTestViewSet, PerformanceViewSet

router = DefaultRouter()
router.register(r'events', AnalyticsViewSet)
router.register(r'ab-tests', ABTestViewSet)
router.register(r'performance', PerformanceViewSet, basename='performance')

urlpatterns = [
    path('api/analytics/', include(router.urls)),
]
