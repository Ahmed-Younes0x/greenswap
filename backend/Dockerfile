FROM python:3.11-slim

# تثبيت المتطلبات النظام
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# إعداد متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# إنشاء مجلد العمل
WORKDIR /app

# نسخ متطلبات Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . /app/

# إنشاء مجلدات الملفات
RUN mkdir -p /app/media /app/staticfiles

# تشغيل collectstatic
RUN python manage.py collectstatic --noinput

# إعطاء صلاحيات للسكريبت
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
