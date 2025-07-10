import re
import magic
import hashlib
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class SecureInputValidator:
    """مدقق شامل للمدخلات"""
    
    # أنماط الهجمات الشائعة
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\bUNION\s+SELECT\b)",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>.*?</iframe>",
        r"<object[^>]*>.*?</object>",
        r"<embed[^>]*>.*?</embed>",
    ]
    
    @classmethod
    def validate_input(cls, value, field_name="input"):
        """التحقق من صحة المدخل"""
        if not isinstance(value, str):
            return value
        
        # فحص SQL Injection
        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                raise ValidationError(
                    f"مدخل غير آمن في حقل {field_name}: محتوى مشبوه تم اكتشافه"
                )
        
        # فحص XSS
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                raise ValidationError(
                    f"مدخل غير آمن في حقل {field_name}: كود ضار تم اكتشافه"
                )
        
        return value
    
    @classmethod
    def sanitize_html(cls, value):
        """تنظيف HTML من العناصر الضارة"""
        import bleach
        
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li']
        allowed_attributes = {}
        
        return bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes)

class FileUploadValidator:
    """مدقق رفع الملفات"""
    
    ALLOWED_EXTENSIONS = {
        'images': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
        'documents': ['pdf', 'doc', 'docx', 'txt'],
        'archives': ['zip', 'rar', '7z'],
    }
    
    DANGEROUS_EXTENSIONS = [
        'exe', 'bat', 'cmd', 'com', 'pif', 'scr', 'vbs', 'js', 'jar',
        'php', 'asp', 'aspx', 'jsp', 'py', 'pl', 'sh', 'ps1'
    ]
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_file(cls, uploaded_file, allowed_types=['images']):
        """التحقق من صحة الملف المرفوع"""
        # فحص الحجم
        if uploaded_file.size > cls.MAX_FILE_SIZE:
            raise ValidationError("حجم الملف كبير جداً (الحد الأقصى 10MB)")
        
        # فحص الامتداد
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension in cls.DANGEROUS_EXTENSIONS:
            raise ValidationError("نوع الملف غير مسموح")
        
        # فحص الامتدادات المسموحة
        allowed_extensions = []
        for file_type in allowed_types:
            allowed_extensions.extend(cls.ALLOWED_EXTENSIONS.get(file_type, []))
        
        if file_extension not in allowed_extensions:
            raise ValidationError(f"امتداد الملف غير مسموح. الامتدادات المسموحة: {', '.join(allowed_extensions)}")
        
        # فحص نوع الملف الحقيقي
        file_content = uploaded_file.read(1024)
        uploaded_file.seek(0)  # إعادة تعيين المؤشر
        
        try:
            mime_type = magic.from_buffer(file_content, mime=True)
            if not cls.is_safe_mime_type(mime_type, file_extension):
                raise ValidationError("نوع الملف لا يتطابق مع امتداده")
        except:
            pass  # في حالة عدم توفر python-magic
        
        # فحص محتوى الملف للبحث عن كود ضار
        if cls.contains_malicious_content(file_content):
            raise ValidationError("الملف يحتوي على محتوى ضار")
        
        return uploaded_file
    
    @classmethod
    def is_safe_mime_type(cls, mime_type, extension):
        """فحص تطابق نوع MIME مع الامتداد"""
        safe_mime_types = {
            'jpg': ['image/jpeg'],
            'jpeg': ['image/jpeg'],
            'png': ['image/png'],
            'gif': ['image/gif'],
            'pdf': ['application/pdf'],
            'txt': ['text/plain'],
        }
        
        expected_types = safe_mime_types.get(extension, [])
        return mime_type in expected_types if expected_types else True
    
    @classmethod
    def contains_malicious_content(cls, content):
        """فحص المحتوى للبحث عن كود ضار"""
        malicious_patterns = [
            b'<script',
            b'javascript:',
            b'<?php',
            b'<%',
            b'eval(',
            b'exec(',
            b'system(',
        ]
        
        content_lower = content.lower()
        return any(pattern in content_lower for pattern in malicious_patterns)
    
    @classmethod
    def generate_file_hash(cls, uploaded_file):
        """توليد hash للملف للتحقق من التكرار"""
        hasher = hashlib.sha256()
        for chunk in uploaded_file.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

# مدققات مخصصة للحقول
username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_\u0600-\u06FF]+$',
    message='اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط'
)

phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{1,14}$',
    message='رقم الهاتف غير صحيح'
)

password_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
    message='كلمة المرور يجب أن تحتوي على 8 أحرف على الأقل، حرف كبير، حرف صغير، رقم، ورمز خاص'
)
