from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationMarkAsReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        notification.is_read = True
        notification.save()
        return Response(self.get_serializer(notification).data)

class NotificationMarkAllAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all marked as read'})
