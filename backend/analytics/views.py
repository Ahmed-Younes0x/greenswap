from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from datetime import timedelta
from .models import AnalyticsEvent, ABTest, PerformanceMetric, ErrorLog
from .services import AnalyticsService, ABTestingService, PerformanceMonitoringService
from .serializers import AnalyticsEventSerializer, ABTestSerializer, PerformanceMetricSerializer
import json

class AnalyticsViewSet(viewsets.ModelViewSet):
    """API للتحليلات"""
    queryset = AnalyticsEvent.objects.all()
    serializer_class = AnalyticsEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """صلاحيات مختلفة حسب العملية"""
        if self.action in ['dashboard', 'track_event']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    @action(detail=False, methods=['post'])
    def track_event(self, request):
        """تتبع حدث جديد"""
        try:
            event_type = request.data.get('event_type')
            event_name = request.data.get('event_name')
            properties = request.data.get('properties', {})
            
            event = AnalyticsService.track_event(
                event_type=event_type,
                event_name=event_name,
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.session_key,
                properties=properties,
                request=request
            )
            
            if event:
                return Response({'status': 'success', 'event_id': str(event.id)})
            else:
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """بيانات لوحة التحكم"""
        try:
            days = int(request.query_params.get('days', 30))
            start_date = timezone.now() - timedelta(days=days)
            
            data = AnalyticsService.get_dashboard_data(start_date=start_date)
            
            return Response(data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def user_behavior(self, request):
        """تحليل سلوك المستخدمين"""
        try:
            days = int(request.query_params.get('days', 7))
            start_date = timezone.now() - timedelta(days=days)
            
            # مسار المستخدم
            user_journey = AnalyticsEvent.objects.filter(
                user=request.user,
                timestamp__gte=start_date
            ).order_by('timestamp').values(
                'event_type', 'event_name', 'page_url', 'timestamp'
            )
            
            # الصفحات الأكثر زيارة
            top_pages = AnalyticsEvent.objects.filter(
                user=request.user,
                event_type='page_view',
                timestamp__gte=start_date
            ).values('page_url').annotate(
                visits=models.Count('id')
            ).order_by('-visits')[:10]
            
            return Response({
                'user_journey': list(user_journey),
                'top_pages': list(top_pages)
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ABTestViewSet(viewsets.ModelViewSet):
    """API لاختبارات A/B"""
    queryset = ABTest.objects.all()
    serializer_class = ABTestSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def assign_variant(self, request, pk=None):
        """تعيين متغير للمستخدم"""
        try:
            test = self.get_object()
            
            variant = ABTestingService.assign_variant(
                test_name=test.name,
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.session_key
            )
            
            return Response({'variant': variant})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def track_conversion(self, request, pk=None):
        """تتبع التحويل"""
        try:
            test = self.get_object()
            value = request.data.get('value')
            
            success = ABTestingService.track_conversion(
                test_name=test.name,
                user=request.user if request.user.is_authenticated else None,
                session_id=request.session.session_key,
                value=value
            )
            
            return Response({'success': success})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """نتائج الاختبار"""
        try:
            test = self.get_object()
            results = ABTestingService.get_test_results(test.name)
            
            return Response(results)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PerformanceViewSet(viewsets.ViewSet):
    """API لمراقبة الأداء"""
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['post'])
    def record_metric(self, request):
        """تسجيل مقياس أداء"""
        try:
            metric_type = request.data.get('metric_type')
            metric_name = request.data.get('metric_name')
            value = float(request.data.get('value'))
            unit = request.data.get('unit', 'ms')
            tags = request.data.get('tags', {})
            
            PerformanceMonitoringService.record_metric(
                metric_type=metric_type,
                metric_name=metric_name,
                value=value,
                unit=unit,
                tags=tags
            )
            
            return Response({'status': 'success'})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """ملخص الأداء"""
        try:
            hours = int(request.query_params.get('hours', 24))
            summary = PerformanceMonitoringService.get_performance_summary(hours)
            
            return Response(summary)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def real_time(self, request):
        """مراقبة الأداء في الوقت الفعلي"""
        try:
            # آخر 5 دقائق
            start_time = timezone.now() - timedelta(minutes=5)
            
            recent_metrics = PerformanceMetric.objects.filter(
                timestamp__gte=start_time
            ).order_by('-timestamp')[:100]
            
            serializer = PerformanceMetricSerializer(recent_metrics, many=True)
            
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
