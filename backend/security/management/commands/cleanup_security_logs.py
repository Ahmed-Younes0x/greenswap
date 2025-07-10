from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from security.models import SecurityLog, RateLimitRecord, FileUploadLog

class Command(BaseCommand):
    help = 'تنظيف سجلات الأمان القديمة'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='الاحتفاظ بالسجلات لعدد الأيام (افتراضي: 90)'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='عرض ما سيتم حذفه دون تنفيذ الحذف'
        )
    
    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        self.stdout.write(f'تنظيف السجلات الأقدم من {cutoff_date}...')
        
        # حساب عدد السجلات التي ستحذف
        security_logs_count = SecurityLog.objects.filter(timestamp__lt=cutoff_date).count()
        rate_limit_count = RateLimitRecord.objects.filter(window_start__lt=cutoff_date).count()
        file_logs_count = FileUploadLog.objects.filter(uploaded_at__lt=cutoff_date).count()
        
        total_count = security_logs_count + rate_limit_count + file_logs_count
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[تشغيل تجريبي] سيتم حذف:\n'
                    f'  - {security_logs_count} سجل أمان\n'
                    f'  - {rate_limit_count} سجل حدود طلبات\n'
                    f'  - {file_logs_count} سجل رفع ملفات\n'
                    f'المجموع: {total_count} سجل'
                )
            )
        else:
            # تنفيذ الحذف
            deleted_security = SecurityLog.objects.filter(timestamp__lt=cutoff_date).delete()
            deleted_rate_limit = RateLimitRecord.objects.filter(window_start__lt=cutoff_date).delete()
            deleted_file_logs = FileUploadLog.objects.filter(uploaded_at__lt=cutoff_date).delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'تم حذف:\n'
                    f'  - {deleted_security[0]} سجل أمان\n'
                    f'  - {deleted_rate_limit[0]} سجل حدود طلبات\n'
                    f'  - {deleted_file_logs[0]} سجل رفع ملفات\n'
                    f'المجموع: {deleted_security[0] + deleted_rate_limit[0] + deleted_file_logs[0]} سجل'
                )
            )
