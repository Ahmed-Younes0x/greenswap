from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from security.models import SecurityLog, RateLimitRecord
from security.utils import block_ip

class Command(BaseCommand):
    help = 'فحص أمني شامل للنظام'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='عدد الأيام للفحص (افتراضي: 7)'
        )
        
        parser.add_argument(
            '--auto-block',
            action='store_true',
            help='حظر تلقائي للـ IPs المشبوهة'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        auto_block = options['auto_block']
        
        self.stdout.write(f'بدء الفحص الأمني لآخر {days} أيام...')
        
        # تحديد نطاق التاريخ
        since_date = timezone.now() - timedelta(days=days)
        
        # فحص محاولات تسجيل الدخول الفاشلة
        failed_logins = self.check_failed_logins(since_date, auto_block)
        
        # فحص الطلبات المشبوهة
        suspicious_requests = self.check_suspicious_requests(since_date, auto_block)
        
        # فحص تجاوز حدود الطلبات
        rate_limit_violations = self.check_rate_limit_violations(since_date)
        
        # تقرير النتائج
        self.stdout.write(
            self.style.SUCCESS(
                f'\n=== تقرير الفحص الأمني ===\n'
                f'محاولات تسجيل دخول فاشلة: {failed_logins}\n'
                f'طلبات مشبوهة: {suspicious_requests}\n'
                f'تجاوز حدود الطلبات: {rate_limit_violations}\n'
            )
        )
    
    def check_failed_logins(self, since_date, auto_block):
        """فحص محاولات تسجيل الدخول الفاشلة"""
        failed_logs = SecurityLog.objects.filter(
            event_type='failed_login',
            timestamp__gte=since_date
        )
        
        # تجميع حسب IP
        ip_failures = {}
        for log in failed_logs:
            ip = log.ip_address
            ip_failures[ip] = ip_failures.get(ip, 0) + 1
        
        # البحث عن IPs مشبوهة (أكثر من 10 محاولات فاشلة)
        suspicious_ips = {ip: count for ip, count in ip_failures.items() if count > 10}
        
        if suspicious_ips:
            self.stdout.write(
                self.style.WARNING(
                    f'تم العثور على {len(suspicious_ips)} عنوان IP مشبوه:'
                )
            )
            
            for ip, count in suspicious_ips.items():
                self.stdout.write(f'  - {ip}: {count} محاولة فاشلة')
                
                if auto_block:
                    block_ip(ip, duration=86400)  # حظر لمدة 24 ساعة
                    self.stdout.write(
                        self.style.SUCCESS(f'    تم حظر {ip} تلقائياً')
                    )
        
        return len(failed_logs)
    
    def check_suspicious_requests(self, since_date, auto_block):
        """فحص الطلبات المشبوهة"""
        suspicious_logs = SecurityLog.objects.filter(
            event_type='suspicious_activity',
            timestamp__gte=since_date
        )
        
        if suspicious_logs.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'تم العثور على {suspicious_logs.count()} طلب مشبوه'
                )
            )
            
            # تجميع حسب IP
            ip_counts = {}
            for log in suspicious_logs:
                ip = log.ip_address
                ip_counts[ip] = ip_counts.get(ip, 0) + 1
            
            for ip, count in ip_counts.items():
                if count > 5:  # أكثر من 5 طلبات مشبوهة
                    self.stdout.write(f'  - {ip}: {count} طلب مشبوه')
                    
                    if auto_block:
                        block_ip(ip, duration=43200)  # حظر لمدة 12 ساعة
                        self.stdout.write(
                            self.style.SUCCESS(f'    تم حظر {ip} تلقائياً')
                        )
        
        return suspicious_logs.count()
    
    def check_rate_limit_violations(self, since_date):
        """فحص تجاوز حدود الطلبات"""
        violations = SecurityLog.objects.filter(
            event_type='rate_limit_exceeded',
            timestamp__gte=since_date
        )
        
        if violations.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'تم العثور على {violations.count()} تجاوز لحدود الطلبات'
                )
            )
        
        return violations.count()
