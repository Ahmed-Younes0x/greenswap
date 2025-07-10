from django.urls import path
from .views import NotificationListView, NotificationMarkAsReadView, NotificationMarkAllAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationMarkAsReadView.as_view(), name='notification-mark-as-read'),
    path('mark-all-read/', NotificationMarkAllAsReadView.as_view(), name='notification-mark-all-as-read'),
]
