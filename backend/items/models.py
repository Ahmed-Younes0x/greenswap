from django.db import models
from django.contrib.gis.db import models as gis_models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_ar = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name_ar

class Item(models.Model):
    CONDITION_CHOICES = [
        ('excellent', 'ممتاز'),
        ('good', 'جيد'),
        ('fair', 'مقبول'),
        ('poor', 'يحتاج إصلاح'),
        ('scrap', 'خردة'),
    ]

    PRICE_TYPE_CHOICES = [
        ('free', 'مجاني'),
        ('fixed', 'سعر ثابت'),
        ('negotiable', 'قابل للتفاوض'),
    ]

    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('pending', 'في الانتظار'),
        ('sold', 'تم البيع'),
        ('expired', 'منتهي الصلاحية'),
        ('rejected', 'مرفوض'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('phone', 'هاتف فقط'),
        ('chat', 'محادثة فقط'),
        ('both', 'كلاهما'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='free')
    location = models.CharField(max_length=200)
    coordinates = gis_models.PointField(blank=True, null=True)
    contact_method = models.CharField(max_length=20, choices=CONTACT_METHOD_CHOICES, default='both')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    views = models.PositiveIntegerField(default=0)
    interested_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"صورة {self.item.title}"

class ItemReport(models.Model):
    REPORT_TYPES = [
        ('inappropriate_content', 'محتوى غير مناسب'),
        ('fake_item', 'منتج مزيف'),
        ('spam', 'رسائل مزعجة'),
        ('fraud', 'احتيال'),
        ('other', 'أخرى'),
    ]

    STATUS_CHOICES = [
        ('pending', 'معلق'),
        ('resolved', 'محلول'),
        ('rejected', 'مرفوض'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"بلاغ على {self.item.title}"
