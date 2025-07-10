import os
from PIL import Image, ImageOpt
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger('performance')

class ImageOptimizer:
    """محسن الصور"""
    
    @staticmethod
    def optimize_image(image_path, quality=85, max_width=1920, max_height=1080):
        """تحسين وضغط الصورة"""
        try:
            with Image.open(image_path) as img:
                # تحويل إلى RGB إذا كانت RGBA
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # تغيير الحجم إذا كان كبيراً
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # حفظ مع ضغط
                optimized_path = image_path.replace('.', '_optimized.')
                img.save(optimized_path, 'JPEG', quality=quality, optimize=True)
                
                return optimized_path
                
        except Exception as e:
            logger.error(f"Image optimization error: {e}")
            return image_path
    
    @staticmethod
    def create_thumbnails(image_path, sizes=[(150, 150), (300, 300), (600, 600)]):
        """إنشاء صور مصغرة بأحجام مختلفة"""
        thumbnails = {}
        
        try:
            with Image.open(image_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                for width, height in sizes:
                    thumbnail = img.copy()
                    thumbnail.thumbnail((width, height), Image.Resampling.LANCZOS)
                    
                    thumb_path = image_path.replace('.', f'_{width}x{height}.')
                    thumbnail.save(thumb_path, 'JPEG', quality=85, optimize=True)
                    thumbnails[f'{width}x{height}'] = thumb_path
                
                return thumbnails
                
        except Exception as e:
            logger.error(f"Thumbnail creation error: {e}")
            return {}

class CDNManager:
    """إدارة CDN"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.cloudfront_domain = getattr(settings, 'CLOUDFRONT_DOMAIN', '')
    
    def upload_to_cdn(self, file_path, s3_key):
        """رفع ملف إلى CDN"""
        try:
            self.s3_client.upload_file(
                file_path, 
                self.bucket_name, 
                s3_key,
                ExtraArgs={
                    'ContentType': self._get_content_type(file_path),
                    'CacheControl': 'max-age=31536000',  # سنة واحدة
                }
            )
            
            if self.cloudfront_domain:
                return f"https://{self.cloudfront_domain}/{s3_key}"
            else:
                return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
                
        except ClientError as e:
            logger.error(f"CDN upload error: {e}")
            return None
    
    def _get_content_type(self, file_path):
        """تحديد نوع المحتوى"""
        extension = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.pdf': 'application/pdf',
            '.mp4': 'video/mp4',
        }
        return content_types.get(extension, 'application/octet-stream')

class DatabaseOptimizer:
    """محسن قاعدة البيانات"""
    
    @staticmethod
    def optimize_queryset(queryset):
        """تحسين QuerySet"""
        # إضافة select_related و prefetch_related تلقائياً
        model = queryset.model
        
        # البحث عن العلاقات
        foreign_keys = [
            field.name for field in model._meta.fields 
            if field.many_to_one
        ]
        
        many_to_many = [
            field.name for field in model._meta.many_to_many
        ]
        
        # تطبيق التحسينات
        if foreign_keys:
            queryset = queryset.select_related(*foreign_keys)
        
        if many_to_many:
            queryset = queryset.prefetch_related(*many_to_many)
        
        return queryset
    
    @staticmethod
    def get_slow_queries():
        """الحصول على الاستعلامات البطيئة"""
        from .models import QueryPerformance
        return QueryPerformance.objects.filter(
            execution_time__gt=0.1
        ).order_by('-execution_time')[:20]
