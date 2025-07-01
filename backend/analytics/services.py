import json
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from django.core.cache import cache
from .models import AnalyticsEvent, UserSession, ABTest, ABTestParticipant, PerformanceMetric, ErrorLog
import logging
import hashlib
import random

logger = logging.getLogger('analytics')

class AnalyticsService:
    """خدمة التحليلات الرئيسية"""
    
    @staticmethod
    def track_event(event_type, event_name, user=None, session_id=None, properties=None, request=None):
        """تتبع حدث جديد"""
        try:
            event_data = {
                'event_type': event_type,
                'event_name': event_name,
                'user': user,
                'session_id': session_id,
                'properties': properties or {},
                'timestamp': timezone.now()
            }
            
            if request:
                event_data.update({
                    'page_url': request.build_absolute_uri(),
                    'referrer': request.META.get('HTTP_REFERER'),
                    'user_agent': request.META.get('HTTP_USER_AGENT'),
                    'ip_address': AnalyticsService.get_client_ip(request),
                })
                
                # تحليل معلومات الجهاز
                device_info = AnalyticsService.parse_user_agent(request.META.get('HTTP_USER_AGENT', ''))
                event_data.update(device_info)
            
            # حفظ في قاعدة البيانات
            event = AnalyticsEvent.objects.create(**event_data)
            
            # إرسال إلى Google Analytics
            AnalyticsService.send_to_google_analytics(event_data)
            
            # إرسال إلى خدمات أخرى
            AnalyticsService.send_to_custom_analytics(event_data)
            
            return event
            
        except Exception as e:
            logger.error(f"Error tracking event: {e}")
            return None
    
    @staticmethod
    def get_client_ip(request):
        """الحصول على IP العميل"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def parse_user_agent(user_agent):
        """تحليل معلومات المتصفح والجهاز"""
        # يمكن استخدام مكتبة user-agents للتحليل المتقدم
        device_info = {
            'device_type': 'desktop',
            'browser': 'unknown',
            'os': 'unknown'
        }
        
        if 'Mobile' in user_agent:
            device_info['device_type'] = 'mobile'
        elif 'Tablet' in user_agent:
            device_info['device_type'] = 'tablet'
            
        if 'Chrome' in user_agent:
            device_info['browser'] = 'chrome'
        elif 'Firefox' in user_agent:
            device_info['browser'] = 'firefox'
        elif 'Safari' in user_agent:
            device_info['browser'] = 'safari'
            
        return device_info
    
    @staticmethod
    def send_to_google_analytics(event_data):
        """إرسال البيانات إلى Google Analytics"""
        try:
            if not settings.GOOGLE_ANALYTICS_ID:
                return
                
            # Google Analytics 4 Measurement Protocol
            url = f"https://www.google-analytics.com/mp/collect"
            
            payload = {
                'client_id': event_data.get('session_id', 'anonymous'),
                'events': [{
                    'name': event_data['event_name'],
                    'params': event_data.get('properties', {})
                }]
            }
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            params = {
                'measurement_id': settings.GOOGLE_ANALYTICS_ID,
                'api_secret': settings.GOOGLE_ANALYTICS_SECRET,
            }
            
            requests.post(url, json=payload, headers=headers, params=params, timeout=5)
            
        except Exception as e:
            logger.error(f"Error sending to Google Analytics: {e}")
    
    @staticmethod
    def send_to_custom_analytics(event_data):
        """إرسال البيانات إلى نظام التحليلات المخصص"""
        try:
            # يمكن إرسال البيانات إلى Mixpanel, Amplitude, أو أي خدمة أخرى
            pass
        except Exception as e:
            logger.error(f"Error sending to custom analytics: {e}")
    
    @staticmethod
    def get_dashboard_data(start_date=None, end_date=None):
        """الحصول على بيانات لوحة التحكم"""
        if not start_date:
            start_date = timezone.now() - timedelta(days=30)
        if not end_date:
            end_date = timezone.now()
        
        cache_key = f"dashboard_data_{start_date.date()}_{end_date.date()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # إحصائيات عامة
        total_events = AnalyticsEvent.objects.filter(
            timestamp__range=[start_date, end_date]
        ).count()
        
        unique_users = AnalyticsEvent.objects.filter(
            timestamp__range=[start_date, end_date],
            user__isnull=False
        ).values('user').distinct().count()
        
        # أهم الصفحات
        top_pages = AnalyticsEvent.objects.filter(
            timestamp__range=[start_date, end_date],
            event_type='page_view'
        ).values('page_url').annotate(
            views=Count('id')
        ).order_by('-views')[:10]
        
        # الأحداث الأكثر شيوعاً
        top_events = AnalyticsEvent.objects.filter(
            timestamp__range=[start_date, end_date]
        ).values('event_name').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # إحصائيات الأجهزة
        device_stats = AnalyticsEvent.objects.filter(
            timestamp__range=[start_date, end_date]
        ).values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # إحصائيات المتصفحات
        browser_stats = AnalyticsEvent.objects.filter(
            timestamp__range=[start_date, end_date]
        ).values('browser').annotate(
            count=Count('id')
        ).order_by('-count')
        
        data = {
            'total_events': total_events,
            'unique_users': unique_users,
            'top_pages': list(top_pages),
            'top_events': list(top_events),
            'device_stats': list(device_stats),
            'browser_stats': list(browser_stats),
            'generated_at': timezone.now()
        }
        
        # حفظ في الكاش لمدة ساعة
        cache.set(cache_key, data, 3600)
        
        return data

class ABTestingService:
    """خدمة اختبارات A/B"""
    
    @staticmethod
    def assign_variant(test_name, user=None, session_id=None):
        """تعيين متغير للمستخدم في اختبار A/B"""
        try:
            test = ABTest.objects.get(name=test_name, is_active=True)
            
            # التحقق من وجود تعيين سابق
            participant = ABTestParticipant.objects.filter(
                test=test,
                user=user,
                session_id=session_id
            ).first()
            
            if participant:
                return participant.variant
            
            # تعيين متغير جديد
            variant = ABTestingService.select_variant(test)
            
            ABTestParticipant.objects.create(
                test=test,
                user=user,
                session_id=session_id,
                variant=variant
            )
            
            return variant
            
        except ABTest.DoesNotExist:
            return 'control'  # المتغير الافتراضي
        except Exception as e:
            logger.error(f"Error assigning A/B test variant: {e}")
            return 'control'
    
    @staticmethod
    def select_variant(test):
        """اختيار متغير بناءً على توزيع الحركة"""
        variants = test.variants
        allocation = test.traffic_allocation
        
        # إنشاء قائمة مرجحة
        weighted_variants = []
        for variant in variants:
            weight = allocation.get(variant, 0)
            weighted_variants.extend([variant] * weight)
        
        if not weighted_variants:
            return variants[0] if variants else 'control'
        
        return random.choice(weighted_variants)
    
    @staticmethod
    def track_conversion(test_name, user=None, session_id=None, value=None):
        """تتبع التحويل في اختبار A/B"""
        try:
            test = ABTest.objects.get(name=test_name, is_active=True)
            
            participant = ABTestParticipant.objects.filter(
                test=test,
                user=user,
                session_id=session_id
            ).first()
            
            if participant and not participant.converted:
                participant.converted = True
                participant.conversion_value = value
                participant.save()
                
                return True
                
        except Exception as e:
            logger.error(f"Error tracking A/B test conversion: {e}")
            
        return False
    
    @staticmethod
    def get_test_results(test_name):
        """الحصول على نتائج اختبار A/B"""
        try:
            test = ABTest.objects.get(name=test_name)
            
            results = {}
            for variant in test.variants:
                participants = ABTestParticipant.objects.filter(
                    test=test,
                    variant=variant
                )
                
                total_participants = participants.count()
                conversions = participants.filter(converted=True).count()
                conversion_rate = (conversions / total_participants * 100) if total_participants > 0 else 0
                
                results[variant] = {
                    'participants': total_participants,
                    'conversions': conversions,
                    'conversion_rate': round(conversion_rate, 2)
                }
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting A/B test results: {e}")
            return {}

class PerformanceMonitoringService:
    """خدمة مراقبة الأداء"""
    
    @staticmethod
    def record_metric(metric_type, metric_name, value, unit='ms', tags=None, metadata=None):
        """تسجيل مقياس أداء"""
        try:
            PerformanceMetric.objects.create(
                metric_type=metric_type,
                metric_name=metric_name,
                value=value,
                unit=unit,
                tags=tags or {},
                metadata=metadata or {}
            )
            
            # إرسال إلى New Relic
            PerformanceMonitoringService.send_to_newrelic(metric_type, metric_name, value, tags)
            
        except Exception as e:
            logger.error(f"Error recording performance metric: {e}")
    
    @staticmethod
    def send_to_newrelic(metric_type, metric_name, value, tags=None):
        """إرسال المقاييس إلى New Relic"""
        try:
            if not settings.NEW_RELIC_LICENSE_KEY:
                return
            
            url = "https://metric-api.newrelic.com/metric/v1"
            
            headers = {
                'Content-Type': 'application/json',
                'Api-Key': settings.NEW_RELIC_LICENSE_KEY
            }
            
            payload = [{
                'metrics': [{
                    'name': f"custom.{metric_type}.{metric_name}",
                    'type': 'gauge',
                    'value': value,
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'attributes': tags or {}
                }]
            }]
            
            requests.post(url, json=payload, headers=headers, timeout=5)
            
        except Exception as e:
            logger.error(f"Error sending to New Relic: {e}")
    
    @staticmethod
    def get_performance_summary(hours=24):
        """الحصول على ملخص الأداء"""
        start_time = timezone.now() - timedelta(hours=hours)
        
        metrics = PerformanceMetric.objects.filter(
            timestamp__gte=start_time
        )
        
        summary = {}
        
        for metric_type in ['page_load_time', 'api_response_time', 'database_query_time']:
            type_metrics = metrics.filter(metric_type=metric_type)
            
            if type_metrics.exists():
                summary[metric_type] = {
                    'avg': type_metrics.aggregate(Avg('value'))['value__avg'],
                    'min': type_metrics.aggregate(models.Min('value'))['value__min'],
                    'max': type_metrics.aggregate(models.Max('value'))['value__max'],
                    'count': type_metrics.count()
                }
        
        return summary

class ErrorTrackingService:
    """خدمة تتبع الأخطاء"""
    
    @staticmethod
    def log_error(level, message, exception=None, user=None, request=None, extra_data=None):
        """تسجيل خطأ جديد"""
        try:
            error_data = {
                'level': level,
                'message': message,
                'user': user,
                'extra_data': extra_data or {}
            }
            
            if exception:
                error_data.update({
                    'exception_type': type(exception).__name__,
                    'stack_trace': str(exception)
                })
            
            if request:
                error_data.update({
                    'session_id': request.session.session_key,
                    'request_url': request.build_absolute_uri(),
                    'request_method': request.method
                })
            
            error = ErrorLog.objects.create(**error_data)
            
            # إرسال إلى Sentry
            ErrorTrackingService.send_to_sentry(error_data, exception)
            
            return error
            
        except Exception as e:
            logger.error(f"Error logging error: {e}")
            return None
    
    @staticmethod
    def send_to_sentry(error_data, exception=None):
        """إرسال الخطأ إلى Sentry"""
        try:
            import sentry_sdk
            
            with sentry_sdk.push_scope() as scope:
                # إضافة معلومات إضافية
                scope.set_tag("level", error_data['level'])
                scope.set_context("error_data", error_data)
                
                if error_data.get('user'):
                    scope.set_user({
                        "id": error_data['user'].id,
                        "email": error_data['user'].email
                    })
                
                if exception:
                    sentry_sdk.capture_exception(exception)
                else:
                    sentry_sdk.capture_message(error_data['message'])
                    
        except Exception as e:
            logger.error(f"Error sending to Sentry: {e}")
