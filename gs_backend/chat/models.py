from django.db import models
from django.conf import settings

class Item(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="items/")

    def __str__(self):
        return self.title

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="conversations")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation on {self.item.title}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, default="text")  # For future extensibility

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
