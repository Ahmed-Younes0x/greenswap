# دليل إعداد وتشغيل مشروع GreenSwap Egypt

## 📋 المتطلبات الأساسية

### 1. تثبيت Node.js
- قم بتحميل Node.js من [الموقع الرسمي](https://nodejs.org/)
- اختر الإصدار LTS (الموصى به)
- تأكد من تثبيت npm معه

### 2. تثبيت Git
- قم بتحميل Git من [الموقع الرسمي](https://git-scm.com/)
- اتبع تعليمات التثبيت حسب نظام التشغيل

### 3. محرر النصوص
- **VS Code** (موصى به): [تحميل](https://code.visualstudio.com/)
- أو أي محرر نصوص آخر

## 🚀 خطوات الإعداد

### الخطوة 1: تحميل المشروع

#### الطريقة الأولى: استنساخ من Git
\`\`\`bash
# فتح Terminal أو Command Prompt
# الانتقال للمجلد المرغوب
cd Desktop

# استنساخ المشروع
git clone https://github.com/your-username/greenswap-egypt.git

# الدخول لمجلد المشروع
cd greenswap-egypt
\`\`\`

#### الطريقة الثانية: تحميل ملف ZIP
1. قم بتحميل المشروع كملف ZIP
2. فك الضغط في المجلد المرغوب
3. افتح Terminal في مجلد المشروع

### الخطوة 2: تثبيت المتطلبات

\`\`\`bash
# تثبيت جميع الحزم المطلوبة
npm install

# في حالة ظهور أخطاء، جرب:
npm install --legacy-peer-deps

# أو استخدم yarn إذا كان متاحاً
yarn install
\`\`\`

### الخطوة 3: إعداد متغيرات البيئة (اختياري)

\`\`\`bash
# إنشاء ملف .env في جذر المشروع
touch .env

# أو في Windows
echo. > .env
\`\`\`

أضف المتغيرات التالية في ملف `.env`:
\`\`\`env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_MAPS_KEY=your_google_maps_key_here
REACT_APP_FIREBASE_CONFIG=your_firebase_config_here
\`\`\`

### الخطوة 4: تشغيل المشروع

\`\`\`bash
# تشغيل الخادم المحلي
npm start

# أو
yarn start
\`\`\`

### الخطوة 5: فتح المتصفح
- سيفتح المتصفح تلقائياً على `http://localhost:3000`
- إذا لم يفتح، افتح المتصفح يدوياً وانتقل للرابط

## 🔧 إعداد VS Code

### الإضافات الموصى بها:

1. **ES7+ React/Redux/React-Native snippets**
   - معرف: `dsznajder.es7-react-js-snippets`

2. **Prettier - Code formatter**
   - معرف: `esbenp.prettier-vscode`

3. **Auto Rename Tag**
   - معرف: `formulahendry.auto-rename-tag`

4. **Bracket Pair Colorizer**
   - معرف: `coenraads.bracket-pair-colorizer`

5. **GitLens**
   - معرف: `eamodio.gitlens`

### إعداد Prettier:
أنشئ ملف `.prettierrc` في جذر المشروع:
\`\`\`json
{
  "semi": false,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 120
}
\`\`\`

## 🐛 حل المشاكل الشائعة

### مشكلة: npm install فشل

**الحل:**
\`\`\`bash
# مسح cache
npm cache clean --force

# حذف node_modules
rm -rf node_modules
# أو في Windows
rmdir /s node_modules

# حذف package-lock.json
rm package-lock.json
# أو في Windows
del package-lock.json

# إعادة التثبيت
npm install
\`\`\`

### مشكلة: المنفذ 3000 مستخدم

**الحل:**
\`\`\`bash
# تشغيل على منفذ مختلف
PORT=3001 npm start

# أو في Windows
set PORT=3001 && npm start
\`\`\`

### مشكلة: أخطاء ESLint

**الحل:**
\`\`\`bash
# تثبيت ESLint
npm install eslint --save-dev

# إعداد ESLint
npx eslint --init
\`\`\`

### مشكلة: الخطوط العربية لا تظهر

**الحل:**
تأكد من وجود الخط في `public/index.html`:
\`\`\`html
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
\`\`\`

## 📱 اختبار المشروع

### اختبار الوظائف الأساسية:

1. **الصفحة الرئيسية**
   - تحقق من تحميل الإحصائيات
   - تأكد من عرض المنتجات الحديثة

2. **التسجيل**
   - جرب إنشاء حساب جديد
   - اختبر أنواع المستخدمين المختلفة

3. **تسجيل الدخول**
   - استخدم البيانات الوهمية
   - تحقق من إعادة التوجيه للوحة التحكم

4. **إضافة منتج**
   - جرب إضافة منتج جديد
   - اختبر رفع الصور

5. **البحث**
   - اختبر البحث النصي
   - جرب المرشحات المختلفة

6. **المحادثات**
   - اختبر إرسال الرسائل
   - تحقق من التحديث الفوري

## 🔄 تحديث المشروع

\`\`\`bash
# سحب آخر التحديثات
git pull origin main

# تحديث الحزم
npm update

# في حالة إضافة حزم جديدة
npm install
\`\`\`

## 📦 بناء المشروع للإنتاج

\`\`\`bash
# بناء المشروع
npm run build

# اختبار البناء محلياً
npx serve -s build

# أو تثبيت serve عالمياً
npm install -g serve
serve -s build
\`\`\`

## 🌐 نشر المشروع

### نشر على Netlify:
1. قم ببناء المشروع: `npm run build`
2. ارفع مجلد `build` على Netlify
3. اضبط إعدادات البناء

### نشر على Vercel:
1. ثبت Vercel CLI: `npm i -g vercel`
2. قم بتسجيل الدخول: `vercel login`
3. انشر المشروع: `vercel --prod`

### نشر على GitHub Pages:
\`\`\`bash
# تثبيت gh-pages
npm install --save-dev gh-pages

# إضافة scripts في package.json
"homepage": "https://yourusername.github.io/greenswap-egypt",
"predeploy": "npm run build",
"deploy": "gh-pages -d build"

# النشر
npm run deploy
\`\`\`

## 🔐 الأمان

### متغيرات البيئة الحساسة:
- لا تضع مفاتيح API في الكود
- استخدم متغيرات البيئة
- أضف `.env` لملف `.gitignore`

### أفضل الممارسات:
\`\`\`bash
# إنشاء .gitignore
echo "node_modules/" >> .gitignore
echo ".env" >> .gitignore
echo "build/" >> .gitignore
echo ".DS_Store" >> .gitignore
\`\`\`

## 📊 مراقبة الأداء

### أدوات مفيدة:
- **React Developer Tools** - إضافة المتصفح
- **Redux DevTools** - لمراقبة الحالة
- **Lighthouse** - تحليل الأداء
- **Bundle Analyzer** - تحليل حجم الملفات

\`\`\`bash
# تحليل حجم Bundle
npm install --save-dev webpack-bundle-analyzer
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
\`\`\`

## 🤝 المساهمة في المشروع

### إعداد بيئة التطوير:
\`\`\`bash
# إنشاء فرع جديد
git checkout -b feature/new-feature

# إجراء التغييرات
# ...

# إضافة التغييرات
git add .

# إنشاء commit
git commit -m "Add new feature"

# رفع الفرع
git push origin feature/new-feature
\`\`\`

## 📞 الحصول على المساعدة

### الموارد المفيدة:
- [وثائق React](https://reactjs.org/docs)
- [وثائق Bootstrap](https://getbootstrap.com/docs)
- [مجتمع Stack Overflow](https://stackoverflow.com)

### التواصل:
- **البريد الإلكتروني**: support@greenswap-egypt.com
- **GitHub Issues**: لتقرير المشاكل
- **Discord**: للدردشة المباشرة

---

**نصائح إضافية:**
- احتفظ بنسخة احتياطية من عملك
- اختبر التغييرات قبل النشر
- اتبع معايير الكود المتفق عليها
- اكتب تعليقات واضحة في الكود

**بالتوفيق في رحلتك مع GreenSwap Egypt! 🌱**
\`\`\`
