from django.db import models
from django.contrib.auth import get_user_model
from items.models import Item

User = get_user_model()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'item']
        verbose_name = 'إعجاب'
        verbose_name_plural = 'الإعجابات'

    def __str__(self):
        return f'{self.user.name} likes {self.item.title}'

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'item']
        verbose_name = 'مفضلة'
        verbose_name_plural = 'المفضلات'

    def __str__(self):
        return f'{self.user.name} bookmarked {self.item.title}'

class Share(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('copy_link', 'Copy Link'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مشاركة'
        verbose_name_plural = 'المشاركات'

    def __str__(self):
        return f'{self.user.name} shared {self.item.title} on {self.platform}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'التعليقات'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.name} commented on {self.item.title}'

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']
        verbose_name = 'متابعة'
        verbose_name_plural = 'المتابعات'

    def __str__(self):
        return f'{self.follower.name} follows {self.following.name}'

class Report(models.Model):
    REPORT_TYPES = [
        ('spam', 'رسائل مزعجة'),
        ('inappropriate', 'محتوى غير مناسب'),
        ('fake', 'محتوى مزيف'),
        ('harassment', 'تحرش'),
        ('copyright', 'انتهاك حقوق الطبع'),
        ('other', 'أخرى'),
    ]

    CONTENT_TYPES = [
        ('item', 'منتج'),
        ('comment', 'تعليق'),
        ('user', 'مستخدم'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    object_id = models.IntegerField()
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'قيد المراجعة'),
        ('reviewed', 'تمت المراجعة'),
        ('resolved', 'تم الحل'),
        ('dismissed', 'تم الرفض'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed')

    class Meta:
        verbose_name = 'بلاغ'
        verbose_name_plural = 'البلاغات'

    def __str__(self):
        return f'Report by {self.reporter.name} - {self.report_type}'

class SocialActivity(models.Model):
    ACTIVITY_TYPES = [
        ('like', 'إعجاب'),
        ('comment', 'تعليق'),
        ('share', 'مشاركة'),
        ('follow', 'متابعة'),
        ('item_posted', 'نشر منتج'),
        ('item_sold', 'بيع منتج'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=200)
    description_ar = models.CharField(max_length=200)
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'نشاط اجتماعي'
        verbose_name_plural = 'الأنشطة الاجتماعية'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.name} - {self.activity_type}'
