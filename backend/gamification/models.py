from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    streak = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'إحصائيات المستخدم'
        verbose_name_plural = 'إحصائيات المستخدمين'

    def __str__(self):
        return f'{self.user.name} - Level {self.level} - {self.points} points'

    def calculate_level(self):
        """حساب المستوى بناءً على النقاط"""
        return min((self.points // 1000) + 1, 100)

    def update_level(self):
        """تحديث المستوى"""
        new_level = self.calculate_level()
        if new_level > self.level:
            self.level = new_level
            self.save()
            return True
        return False

class Badge(models.Model):
    BADGE_TYPES = [
        ('first_item', 'أول منتج'),
        ('first_sale', 'أول بيع'),
        ('eco_warrior', 'محارب البيئة'),
        ('social_butterfly', 'اجتماعي'),
        ('reviewer', 'مقيم'),
        ('streak_master', 'سيد التتابع'),
        ('top_seller', 'أفضل بائع'),
        ('helper', 'مساعد'),
    ]

    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    description = models.TextField()
    description_ar = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, unique=True)
    icon = models.CharField(max_length=50, default='fa-medal')
    color = models.CharField(max_length=20, default='primary')
    points_required = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'شارة'
        verbose_name_plural = 'الشارات'

    def __str__(self):
        return self.name_ar

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']
        verbose_name = 'شارة المستخدم'
        verbose_name_plural = 'شارات المستخدمين'

    def __str__(self):
        return f'{self.user.name} - {self.badge.name_ar}'

class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('items_posted', 'منتجات منشورة'),
        ('sales_completed', 'مبيعات مكتملة'),
        ('reviews_given', 'تقييمات مقدمة'),
        ('social_interactions', 'تفاعلات اجتماعية'),
        ('streak_days', 'أيام متتالية'),
        ('points_earned', 'نقاط مكتسبة'),
    ]

    title = models.CharField(max_length=100)
    title_ar = models.CharField(max_length=100)
    description = models.TextField()
    description_ar = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    target_value = models.IntegerField()
    points_reward = models.IntegerField()
    badge_reward = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'إنجاز'
        verbose_name_plural = 'الإنجازات'

    def __str__(self):
        return self.title_ar

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    current_progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'achievement']
        verbose_name = 'إنجاز المستخدم'
        verbose_name_plural = 'إنجازات المستخدمين'

    def __str__(self):
        return f'{self.user.name} - {self.achievement.title_ar}'

    def update_progress(self, value):
        """تحديث التقدم في الإنجاز"""
        self.current_progress = min(value, self.achievement.target_value)
        
        if self.current_progress >= self.achievement.target_value and not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            
            # منح النقاط والشارة
            self.user.stats.points += self.achievement.points_reward
            self.user.stats.save()
            
            if self.achievement.badge_reward:
                UserBadge.objects.get_or_create(
                    user=self.user,
                    badge=self.achievement.badge_reward
                )
        
        self.save()

class PointsHistory(models.Model):
    ACTION_TYPES = [
        ('item_posted', 'نشر منتج'),
        ('item_sold', 'بيع منتج'),
        ('review_given', 'تقديم تقييم'),
        ('review_received', 'استلام تقييم'),
        ('social_interaction', 'تفاعل اجتماعي'),
        ('daily_login', 'تسجيل دخول يومي'),
        ('achievement_completed', 'إكمال إنجاز'),
        ('badge_earned', 'كسب شارة'),
        ('referral', 'إحالة'),
        ('bonus', 'مكافأة'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_history')
    action = models.CharField(max_length=30, choices=ACTION_TYPES)
    points = models.IntegerField()
    description = models.CharField(max_length=200)
    description_ar = models.CharField(max_length=200)
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تاريخ النقاط'
        verbose_name_plural = 'تاريخ النقاط'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.name} - {self.points} points - {self.action}'

class DailyChallenge(models.Model):
    CHALLENGE_TYPES = [
        ('post_item', 'نشر منتج'),
        ('give_review', 'تقديم تقييم'),
        ('social_interaction', 'تفاعل اجتماعي'),
        ('complete_sale', 'إكمال بيع'),
        ('browse_items', 'تصفح المنتجات'),
    ]

    title = models.CharField(max_length=100)
    title_ar = models.CharField(max_length=100)
    description = models.TextField()
    description_ar = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    target_value = models.IntegerField()
    points_reward = models.IntegerField()
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تحدي يومي'
        verbose_name_plural = 'التحديات اليومية'
        unique_together = ['challenge_type', 'date']

    def __str__(self):
        return f'{self.title_ar} - {self.date}'

class UserDailyChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    current_progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'challenge']
        verbose_name = 'تحدي يومي للمستخدم'
        verbose_name_plural = 'التحديات اليومية للمستخدمين'

    def __str__(self):
        return f'{self.user.name} - {self.challenge.title_ar}'

class Reward(models.Model):
    REWARD_TYPES = [
        ('discount', 'خصم'),
        ('feature', 'ميزة مميزة'),
        ('badge', 'شارة خاصة'),
        ('points', 'نقاط إضافية'),
        ('priority', 'أولوية في البحث'),
    ]

    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    description = models.TextField()
    description_ar = models.TextField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    cost_points = models.IntegerField()
    value = models.CharField(max_length=100)  # قيمة المكافأة (نسبة خصم، عدد أيام، إلخ)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=-1)  # -1 للمخزون غير المحدود
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مكافأة'
        verbose_name_plural = 'المكافآت'

    def __str__(self):
        return self.name_ar

class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'مكافأة المستخدم'
        verbose_name_plural = 'مكافآت المستخدمين'

    def __str__(self):
        return f'{self.user.name} - {self.reward.name_ar}'
