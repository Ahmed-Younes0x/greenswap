from rest_framework import generics, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class MessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages = conversation.messages.all().order_by("timestamp")
        return Response(MessageSerializer(messages, many=True).data)

    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=request.data.get("content"),
            type="text"
        )
        return Response(MessageSerializer(message).data)
