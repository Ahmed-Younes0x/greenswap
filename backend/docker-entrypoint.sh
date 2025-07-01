#!/bin/bash

# انتظار قاعدة البيانات
echo "انتظار قاعدة البيانات..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done

echo "قاعدة البيانات جاهزة!"

# تشغيل migrations
echo "تشغيل migrations..."
python manage.py migrate

# إنشاء البيانات التجريبية
echo "إنشاء البيانات التجريبية..."
python scripts/seed_data.py

# تشغيل الخادم
echo "تشغيل الخادم..."
if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn greenswap.wsgi:application --bind 0.0.0.0:8000
fi
