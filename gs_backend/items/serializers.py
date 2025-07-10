from rest_framework import serializers
from .models import Category, Item, ItemImage, ItemReport
from accounts.serializers import UserListSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'description', 'icon', 'is_active']

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'is_primary']

class ItemListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'category', 'user', 'condition',
            'price', 'price_type', 'location', 'status', 'views',
            'interested_count', 'primary_image', 'created_at'
        ]

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return self.context['request'].build_absolute_uri(primary_image.image.url)
        return None

class ItemDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'category', 'user', 'condition',
            'quantity', 'unit', 'price', 'price_type', 'location',
            'contact_method', 'status', 'views', 'interested_count',
            'is_featured', 'images', 'created_at', 'updated_at'
        ]

class ItemCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Item
        fields = [
            'title', 'description', 'category', 'condition', 'quantity',
            'unit', 'price', 'price_type', 'location', 'contact_method',
            'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        validated_data['user'] = self.context['request'].user
        item = Item.objects.create(**validated_data)
        
        for i, image_data in enumerate(images_data):
            ItemImage.objects.create(
                item=item,
                image=image_data,
                is_primary=(i == 0)
            )
        
        return item

class ItemReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemReport
        fields = ['id', 'item', 'report_type', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        return super().create(validated_data)
