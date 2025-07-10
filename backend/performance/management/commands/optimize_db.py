from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'تحسين قاعدة البيانات وإضافة الفهارس'

    def add_arguments(self, parser):
        parser.add_argument(
            '--analyze',
            action='store_true',
            help='تحليل الاستعلامات البطيئة',
        )
        parser.add_argument(
            '--create-indexes',
            action='store_true',
            help='إنشاء فهارس محسنة',
        )

    def handle(self, *args, **options):
        if options['analyze']:
            self.analyze_slow_queries()
        
        if options['create_indexes']:
            self.create_optimized_indexes()
        
        self.stdout.write(
            self.style.SUCCESS('تم تحسين قاعدة البيانات بنجاح')
        )

    def analyze_slow_queries(self):
        """تحليل الاستعلامات البطيئة"""
        with connection.cursor() as cursor:
            # PostgreSQL specific
            cursor.execute("""
                SELECT query, mean_time, calls, total_time
                FROM pg_stat_statements
                WHERE mean_time > 100
                ORDER BY mean_time DESC
                LIMIT 10;
            """)
            
            results = cursor.fetchall()
            if results:
                self.stdout.write("الاستعلامات البطيئة:")
                for query, mean_time, calls, total_time in results:
                    self.stdout.write(f"  {mean_time:.2f}ms: {query[:100]}...")

    def create_optimized_indexes(self):
        """إنشاء فهارس محسنة"""
        indexes = [
            # فهارس للمستخدمين
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_location ON accounts_user USING GIN(to_tsvector('arabic', location));",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_user_type_active ON accounts_user(user_type, is_active);",
            
            # فهارس للعناصر
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_items_status_created ON items_item(status, created_at DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_items_category_location ON items_item(category_id, location);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_items_price_range ON items_item(price) WHERE price IS NOT NULL;",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_items_search ON items_item USING GIN(to_tsvector('arabic', title || ' ' || description));",
            
            # فهارس للطلبات
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_status ON orders_order(user_id, status);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_created_status ON orders_order(created_at DESC, status);",
            
            # فهارس للمحادثات
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_messages_conversation_created ON chat_message(conversation_id, created_at DESC);",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_conversations_participants ON chat_conversation_participants(user_id);",
        ]
        
        with connection.cursor() as cursor:
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                    self.stdout.write(f"✓ تم إنشاء الفهرس: {index_sql.split('idx_')[1].split(' ')[0]}")
                except Exception as e:
                    self.stdout.write(f"✗ خطأ في إنشاء الفهرس: {e}")
