from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_orders, name='list_orders'),
    path('<int:order_id>/status/', views.update_order_status, name='update_order_status'),
]
