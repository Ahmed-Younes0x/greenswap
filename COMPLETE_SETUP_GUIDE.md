# دليل الإعداد الكامل - GreenSwap Egypt

## 🚀 النسخة النهائية الجاهزة للاستخدام

تم ربط Frontend بـ Backend بالكامل وإزالة جميع البيانات المحاكاة واستبدالها بـ API حقيقي.

## 📋 المتطلبات

### Backend Requirements:
- Python 3.11+
- PostgreSQL 13+ مع PostGIS
- Redis 6+

### Frontend Requirements:
- Node.js 16+
- npm 8+

## 🔧 الإعداد السريع (Docker)

### 1. تشغيل Backend
\`\`\`bash
cd backend
cp .env.example .env
docker-compose up --build
\`\`\`

### 2. تشغيل Frontend
\`\`\`bash
cd ../
npm install
npm start
\`\`\`

## 🔧 الإعداد المحلي

### 1. إعداد قاعدة البيانات
\`\`\`bash
# تثبيت PostgreSQL مع PostGIS
sudo apt-get install postgresql postgresql-contrib postgis

# إنشاء قاعدة البيانات
sudo -u postgres createdb greenswap_db
sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'admin';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE greenswap_db TO admin;"
sudo -u postgres psql -d greenswap_db -c "CREATE EXTENSION postgis;"
\`\`\`

### 2. إعداد Redis
\`\`\`bash
# تثبيت Redis
sudo apt-get install redis-server

# تشغيل Redis
redis-server
\`\`\`

### 3. إعداد Backend
\`\`\`bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate  # Windows

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد متغيرات البيئة
cp .env.example .env

# تشغيل migrations
python manage.py migrate

# إنشاء البيانات التجريبية
python scripts/seed_data.py

# تشغيل الخادم
python manage.py runserver
\`\`\`

### 4. إعداد Frontend
\`\`\`bash
# في terminal جديد
cd ../

# تثبيت المتطلبات
npm install

# إنشاء ملف البيئة
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# تشغيل التطبيق
npm start
\`\`\`

### 5. تشغيل Celery (اختياري)
\`\`\`bash
# في terminal جديد
cd backend
source venv/bin/activate

# تشغيل Celery Worker
celery -A greenswap worker -l info

# تشغيل Celery Beat (في terminal آخر)
celery -A greenswap beat -l info
\`\`\`

## 🔑 بيانات الدخول

### Admin Panel
- URL: http://localhost:8000/admin
- Username: `admin`
- Password: `admin`

### API Documentation
- URL: http://localhost:8000/api/docs/

### Sample Users
- Username: `ahmed_mohamed` | Password: `password123`
- Username: `workshop_modern` | Password: `password123`
- Username: `plastic_factory` | Password: `password123`
- Username: `green_org` | Password: `password123`

## 📊 نقاط النهاية الرئيسية

### Authentication
- `POST /api/auth/register/` - تسجيل مستخدم جديد
- `POST /api/auth/login/` - تسجيل الدخول
- `POST /api/auth/logout/` - تسجيل الخروج
- `GET /api/auth/current-user/` - المستخدم الحالي
- `PATCH /api/auth/profile/` - تحديث الملف الشخصي

### Items
- `GET /api/items/` - قائمة المنتجات
- `POST /api/items/create/` - إضافة منتج جديد
- `GET /api/items/{id}/` - تفاصيل المنتج
- `GET /api/items/categories/` - قائمة الفئات
- `GET /api/items/featured/` - المنتجات المميزة
- `GET /api/items/stats/` - الإحصائيات

### Orders
- `GET /api/orders/` - قائمة الطلبات
- `POST /api/orders/` - إنشاء طلب جديد
- `GET /api/orders/my-orders/` - طلباتي

### Chat
- `GET /api/chat/conversations/` - المحادثات
- `POST /api/chat/conversations/` - إنشاء محادثة
- `GET /api/chat/conversations/{id}/messages/` - رسائل المحادثة

### Notifications
- `GET /api/notifications/` - الإشعارات
- `PATCH /api/notifications/{id}/` - تحديد كمقروء

## 🔧 المميزات المتاحة

### ✅ تم التنفيذ
- [x] نظام المصادقة الكامل (JWT)
- [x] إدارة المستخدمين
- [x] إدارة المنتجات مع الصور
- [x] البحث والتصفية المتقدم
- [x] نظام الفئات
- [x] الإحصائيات الأساسية
- [x] API موثق بالكامل
- [x] لوحة الإدارة
- [x] Docker Support

### 🚧 قيد التطوير
- [ ] نظام المحادثات الفورية
- [ ] نظام الطلبات الكامل
- [ ] نظام الإشعارات
- [ ] نظام التقييمات
- [ ] الخرائط والمواقع

## 🐛 حل المشاكل الشائعة

### مشكلة: خطأ في الاتصال بقاعدة البيانات
\`\`\`bash
# تأكد من تشغيل PostgreSQL
sudo systemctl start postgresql

# تأكد من إعدادات قاعدة البيانات في .env
\`\`\`

### مشكلة: خطأ في Redis
\`\`\`bash
# تأكد من تشغيل Redis
redis-cli ping
# يجب أن يرجع PONG
\`\`\`

### مشكلة: CORS Error
\`\`\`bash
# تأكد من إضافة Frontend URL في settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
\`\`\`

### مشكلة: 401 Unauthorized
\`\`\`bash
# تأكد من وجود التوكن في localStorage
# أو سجل دخول مرة أخرى
\`\`\`

## 📱 اختبار التطبيق

### 1. تسجيل مستخدم جديد
- انتقل إلى http://localhost:3000/register
- املأ البيانات وسجل

### 2. تسجيل الدخول
- استخدم البيانات التجريبية أو حسابك الجديد

### 3. إضافة منتج
- انتقل إلى "إضافة مخلف"
- املأ البيانات وأضف صور

### 4. البحث والتصفية
- انتقل إلى صفحة البحث
- جرب المرشحات المختلفة

## 🚀 النشر للإنتاج

### Backend (Heroku/DigitalOcean)
\`\`\`bash
# إعداد متغيرات البيئة للإنتاج
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...

# تشغيل مع Gunicorn
gunicorn greenswap.wsgi:application
\`\`\`

### Frontend (Netlify/Vercel)
\`\`\`bash
# بناء المشروع
npm run build

# رفع مجلد build
\`\`\`

## 📞 الدعم

### الموارد المفيدة
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [React Documentation](https://reactjs.org/docs/)

### التواصل
- **GitHub Issues**: لتقرير المشاكل
- **Email**: support@greenswap-egypt.com

---

**🎉 المشروع جاهز للاستخدام والتطوير!**

تم ربط Frontend بـ Backend بالكامل وإزالة جميع البيانات المحاكاة. النظام يعمل الآن مع API حقيقي وقاعدة بيانات PostgreSQL.
