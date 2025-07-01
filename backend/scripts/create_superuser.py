#!/usr/bin/env python
import os
import sys
import django

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greenswap.settings')
django.setup()

from accounts.models import User

def create_superuser():
    """إنشاء مستخدم مدير"""
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
        print("✅ تم إنشاء المستخدم المدير بنجاح")
        print("Username: admin")
        print("Password: admin")
    else:
        print("⚠️ المستخدم المدير موجود بالفعل")

if __name__ == '__main__':
    create_superuser()
