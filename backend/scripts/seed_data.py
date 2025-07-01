#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenswap.settings')
django.setup()

from accounts.models import User
from items.models import Category, Item

def create_categories():
    """إنشاء الفئات الأساسية"""
    categories_data = [
        {'name': 'furniture', 'name_ar': 'أثاث', 'description': 'أثاث مستعمل قابل للإصلاح', 'icon': 'fas fa-couch'},
        {'name': 'electronics', 'name_ar': 'إلكترونيات', 'description': 'أجهزة إلكترونية ومعدات', 'icon': 'fas fa-laptop'},
        {'name': 'metals', 'name_ar': 'معادن', 'description': 'خردة معادن وحديد', 'icon': 'fas fa-industry'},
        {'name': 'plastic', 'name_ar': 'بلاستيك', 'description': 'مواد بلاستيكية قابلة للتدوير', 'icon': 'fas fa-recycle'},
        {'name': 'paper', 'name_ar': 'ورق وكرتون', 'description': 'ورق وكرتون مستعمل', 'icon': 'fas fa-file-alt'},
        {'name': 'glass', 'name_ar': 'زجاج', 'description': 'زجاج قابل للتدوير', 'icon': 'fas fa-wine-glass'},
        {'name': 'textiles', 'name_ar': 'منسوجات', 'description': 'ملابس ومنسوجات مستعملة', 'icon': 'fas fa-tshirt'},
        {'name': 'construction', 'name_ar': 'مواد بناء', 'description': 'مواد بناء مستعملة', 'icon': 'fas fa-hammer'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✅ تم إنشاء فئة: {category.name_ar}")

def create_sample_users():
    """إنشاء مستخدمين تجريبيين"""
    users_data = [
        {
            'username': 'ahmed_mohamed',
            'email': 'ahmed@example.com',
            'password': 'password123',
            'first_name': 'أحمد',
            'last_name': 'محمد',
            'user_type': 'individual',
            'location': 'القاهرة',
            'phone': '01234567890'
        },
        {
            'username': 'workshop_modern',
            'email': 'workshop@example.com',
            'password': 'password123',
            'first_name': 'ورشة',
            'last_name': 'التدوير الحديثة',
            'user_type': 'workshop',
            'location': 'الجيزة',
            'phone': '01234567891',
            'organization': 'ورشة التدوير الحديثة'
        },
        {
            'username': 'plastic_factory',
            'email': 'factory@example.com',
            'password': 'password123',
            'first_name': 'مصنع',
            'last_name': 'البلاستيك',
            'user_type': 'company',
            'location': 'الإسكندرية',
            'phone': '01234567892',
            'organization': 'مصنع البلاستيك المصري'
        },
        {
            'username': 'green_org',
            'email': 'green@example.com',
            'password': 'password123',
            'first_name': 'جمعية',
            'last_name': 'البيئة الخضراء',
            'user_type': 'organization',
            'location': 'الدقهلية',
            'phone': '01234567893',
            'organization': 'جمعية البيئة الخضراء'
        }
    ]
    
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            print(f"✅ تم إنشاء مستخدم: {user.username}")

def create_sample_items():
    """إنشاء منتجات تجريبية"""
    # الحصول على المستخدمين والفئات
    users = User.objects.filter(user_type__in=['individual', 'workshop', 'company'])
    categories = Category.objects.all()
    
    if not users.exists() or not categories.exists():
        print("⚠️ لا توجد مستخدمين أو فئات لإنشاء المنتجات")
        return
    
    items_data = [
        {
            'title': 'أثاث مكتبي مستعمل',
            'description': 'مجموعة من الأثاث المكتبي المستعمل في حالة جيدة جداً. تشمل مكاتب وكراسي وخزانة ملفات.',
            'category': categories.filter(name='furniture').first(),
            'user': users.first(),
            'condition': 'good',
            'quantity': 1,
            'unit': 'مجموعة',
            'price_type': 'free',
            'location': 'القاهرة - مدينة نصر',
            'contact_method': 'both',
            'status': 'active',
            'is_featured': True
        },
        {
            'title': 'أجهزة كمبيوتر قديمة',
            'description': 'أجهزة كمبيوتر قديمة للتدوير أو قطع الغيار. تحتاج إصلاح أو يمكن استخدامها للقطع.',
            'category': categories.filter(name='electronics').first(),
            'user': users.filter(user_type='company').first(),
            'condition': 'poor',
            'quantity': 5,
            'unit': 'قطعة',
            'price': Decimal('500.00'),
            'price_type': 'fixed',
            'location': 'الجيزة',
            'contact_method': 'both',
            'status': 'active',
            'is_featured': True
        },
        {
            'title': 'خردة معادن مختلطة',
            'description': 'كمية كبيرة من خردة المعادن المختلطة. مناسبة لورش التدوير.',
            'category': categories.filter(name='metals').first(),
            'user': users.filter(user_type='workshop').first(),
            'condition': 'scrap',
            'quantity': 100,
            'unit': 'كيلوجرام',
            'price': Decimal('15.00'),
            'price_type': 'negotiable',
            'location': 'الإسكندرية',
            'contact_method': 'phone',
            'status': 'active'
        },
        {
            'title': 'بلاستيك مختلط للتدوير',
            'description': 'أكياس وعبوات بلاستيكية نظيفة ومصنفة. جاهزة لإعادة التدوير.',
            'category': categories.filter(name='plastic').first(),
            'user': users.filter(user_type='organization').first(),
            'condition': 'good',
            'quantity': 50,
            'unit': 'كيس',
            'price': Decimal('200.00'),
            'price_type': 'fixed',
            'location': 'المنصورة',
            'contact_method': 'chat',
            'status': 'active',
            'is_featured': True
        },
        {
            'title': 'كرتون وورق مستعمل',
            'description': 'كمية كبيرة من الكرتون والورق المستعمل. نظيف ومناسب لإعادة التدوير.',
            'category': categories.filter(name='paper').first(),
            'user': users.first(),
            'condition': 'fair',
            'quantity': 20,
            'unit': 'صندوق',
            'price_type': 'free',
            'location': 'القاهرة',
            'contact_method': 'both',
            'status': 'active'
        }
    ]
    
    for item_data in items_data:
        if not Item.objects.filter(title=item_data['title']).exists():
            item = Item.objects.create(**item_data)
            print(f"✅ تم إنشاء منتج: {item.title}")

def main():
    """تشغيل جميع وظائف إنشاء البيانات"""
    print("🌱 بدء إنشاء البيانات التجريبية...")
    
    # إنشاء المستخدم المدير
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@greenswap.com',
            password='admin',
            first_name='مدير',
            last_name='النظام',
            user_type='admin',
            location='القاهرة',
            phone='01234567890'
        )
        print("✅ تم إنشاء المستخدم المدير")
    
    create_categories()
    create_sample_users()
    create_sample_items()
    
    print("\n🎉 تم إنشاء جميع البيانات التجريبية بنجاح!")
    print("\n📋 بيانات الدخول:")
    print("Admin Panel: http://localhost:8000/admin")
    print("Username: admin")
    print("Password: admin")
    print("\nSample Users:")
    print("Username: ahmed_mohamed | Password: password123")
    print("Username: workshop_modern | Password: password123")
    print("Username: plastic_factory | Password: password123")
    print("Username: green_org | Password: password123")

if __name__ == '__main__':
    main()
