from django.contrib import admin
from .models import Category, Item, ItemImage, ItemReport

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'name_ar']

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'condition', 'price_type', 'status', 'views', 'created_at']
    list_filter = ['status', 'condition', 'price_type', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    inlines = [ItemImageInline]
    readonly_fields = ['views', 'interested_count']

@admin.register(ItemReport)
class ItemReportAdmin(admin.ModelAdmin):
    list_display = ['item', 'reporter', 'report_type', 'status', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['item__title', 'reporter__username', 'reason']
