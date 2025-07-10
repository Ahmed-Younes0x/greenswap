import re
import requests
from django.core.cache import cache
from django.conf import settings
from user_agents import parse

def get_client_ip(request):
    """الحصول على عنوان IP الحقيقي للعميل"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_suspicious_request(request):
    """فحص الطلبات المشبوهة"""
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # فحص قائمة IP المحظورة
    if is_blocked_ip(ip):
        return True
    
    # فحص User Agent
    if is_suspicious_user_agent(user_agent):
        return True
    
    # فحص معدل الطلبات
    if is_high_request_rate(ip):
        return True
    
    return False

def is_blocked_ip(ip):
    """فحص IP المحظور"""
    blocked_ips = cache.get('blocked_ips', set())
    return ip in blocked_ips

def is_suspicious_user_agent(user_agent):
    """فحص User Agent المشبوه"""
    if not user_agent:
        return True
    
    suspicious_patterns = [
        r'bot', r'crawler', r'spider', r'scraper',
        r'hack', r'scan', r'exploit', r'attack',
        r'curl', r'wget', r'python-requests'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, user_agent, re.IGNORECASE):
            return True
    
    return False

def is_high_request_rate(ip):
    """فحص معدل الطلبات العالي"""
    cache_key = f"request_rate_{ip}"
    current_count = cache.get(cache_key, 0)
    
    # أكثر من 100 طلب في الدقيقة
    if current_count > 100:
        return True
    
    cache.set(cache_key, current_count + 1, 60)
    return False

def block_ip(ip, duration=3600):
    """حظر عنوان IP"""
    blocked_ips = cache.get('blocked_ips', set())
    blocked_ips.add(ip)
    cache.set('blocked_ips', blocked_ips, duration)

def get_geolocation(ip):
    """الحصول على الموقع الجغرافي لعنوان IP"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'region': data.get('regionName'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon')
                }
    except:
        pass
    return None

def parse_user_agent(user_agent_string):
    """تحليل معلومات User Agent"""
    user_agent = parse(user_agent_string)
    return {
        'browser': user_agent.browser.family,
        'browser_version': user_agent.browser.version_string,
        'os': user_agent.os.family,
        'os_version': user_agent.os.version_string,
        'device': user_agent.device.family,
        'is_mobile': user_agent.is_mobile,
        'is_tablet': user_agent.is_tablet,
        'is_pc': user_agent.is_pc,
        'is_bot': user_agent.is_bot
    }

def sanitize_filename(filename):
    """تنظيف اسم الملف من الأحرف الضارة"""
    # إزالة الأحرف الخطيرة
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # إزالة المسارات النسبية
    filename = filename.replace('..', '')
    
    # تحديد الطول الأقصى
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]
    
    return filename

def generate_secure_token(length=32):
    """توليد رمز آمن"""
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_password_securely(password):
    """تشفير كلمة المرور بطريقة آمنة"""
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed):
    """التحقق من كلمة المرور"""
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
