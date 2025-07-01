from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('', views.ItemListView.as_view(), name='item_list'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('my-items/', views.MyItemsView.as_view(), name='my_items'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('<int:item_id>/interested/', views.mark_interested, name='mark_interested'),
    path('report/', views.ItemReportView.as_view(), name='item_report'),
    path('search/', views.search_items, name='search_items'),
    path('featured/', views.featured_items, name='featured_items'),
    path('stats/', views.stats, name='stats'),
]
