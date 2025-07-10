from django.core.management.base import BaseCommand
from django.core.cache import cache
from items.models import Item, Category
from accounts.models import User
from performance.cache import advanced_cache

class Command(BaseCommand):
    help = 'تسخين الكاش بالبيانات المهمة'

    def handle(self, *args, **options):
        self.stdout.write('بدء تسخين الكاش...')
        
        # كاش الفئات
        categories = list(Category.objects.filter(is_active=True))
        advanced_cache.set('active_categories', categories, 3600)
        self.stdout.write(f'✓ تم كاش {len(categories)} فئة')
        
        # كاش العناصر المميزة
        featured_items = list(Item.objects.filter(is_featured=True, status='active')[:10])
        advanced_cache.set('featured_items', featured_items, 1800)
        self.stdout.write(f'✓ تم كاش {len(featured_items)} عنصر مميز')
        
        # كاش الإحصائيات
        stats = {
            'total_items': Item.objects.filter(status='active').count(),
            'total_users': User.objects.filter(is_active=True).count(),
            'completed_deals': Item.objects.filter(status='sold').count(),
        }
        advanced_cache.set('platform_stats', stats, 3600)
        self.stdout.write('✓ تم كاش الإحصائيات')
        
        self.stdout.write(
            self.style.SUCCESS('تم تسخين الكاش بنجاح')
        )
