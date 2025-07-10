from rest_framework import serializers
from .models import Conversation, Message, Item
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "user_type", "avatar"]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "image"]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp", "type"]

class ConversationSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    user = serializers.SerializerMethodField()
    lastMessage = serializers.SerializerMethodField()
    lastMessageTime = serializers.SerializerMethodField()
    unreadCount = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "user", "item", "lastMessage", "lastMessageTime", "unreadCount"]

    def get_user(self, obj):
        current_user = self.context['request'].user
        other_user = obj.participants.exclude(id=current_user.id).first()
        return UserSerializer(other_user).data

    def get_lastMessage(self, obj):
        last_msg = obj.messages.last()
        return last_msg.content if last_msg else ""

    def get_lastMessageTime(self, obj):
        last_msg = obj.messages.last()
        return last_msg.timestamp if last_msg else None

    def get_unreadCount(self, obj):
        # Placeholder: you'd need logic to track unread messages per user
        return 0
