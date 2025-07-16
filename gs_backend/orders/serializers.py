from rest_framework import serializers
from items.models import Item
from .models import Order
from accounts.serializers import UserProfileSerializer  # assumes you already have a user serializer

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'image', 'category']

class OrderSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    buyer = UserProfileSerializer()
    seller = UserProfileSerializer()

    class Meta:
        model = Order
        fields = '__all__'
