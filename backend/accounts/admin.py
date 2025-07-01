from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'location', 'is_verified', 'rating', 'total_deals']
    list_filter = ['user_type', 'is_verified', 'location', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'organization']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('معلومات إضافية', {
            'fields': ('user_type', 'phone', 'location', 'organization', 'bio', 'avatar', 'coordinates')
        }),
        ('إحصائيات', {
            'fields': ('is_verified', 'rating', 'total_deals')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('معلومات إضافية', {
            'fields': ('user_type', 'phone', 'location', 'organization')
        }),
    )
