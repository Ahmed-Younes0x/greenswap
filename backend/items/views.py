from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Item, ItemReport
from .serializers import (
    CategorySerializer,
    ItemListSerializer,
    ItemDetailSerializer,
    ItemCreateSerializer,
    ItemReportSerializer
)
from .filters import ItemFilter

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.filter(status='active')
    serializer_class = ItemListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ItemFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'views', 'price']
    ordering = ['-created_at']

class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.filter(status='active')
    serializer_class = ItemDetailSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # زيادة عدد المشاهدات
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ItemCreateView(generics.CreateAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyItemsView(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

class ItemUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_interested(request, item_id):
    try:
        item = Item.objects.get(id=item_id, status='active')
        item.interested_count += 1
        item.save(update_fields=['interested_count'])
        return Response({'message': 'تم تسجيل الاهتمام بنجاح'})
    except Item.DoesNotExist:
        return Response({'error': 'المنتج غير موجود'}, status=status.HTTP_404_NOT_FOUND)

class ItemReportView(generics.CreateAPIView):
    serializer_class = ItemReportSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_items(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    price_type = request.GET.get('price_type', '')
    condition = request.GET.get('condition', '')

    items = Item.objects.filter(status='active')

    if query:
        items = items.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if category:
        items = items.filter(category__name=category)

    if location:
        items = items.filter(location__icontains=location)

    if price_type:
        items = items.filter(price_type=price_type)

    if condition:
        items = items.filter(condition=condition)

    serializer = ItemListSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_items(request):
    items = Item.objects.filter(status='active', is_featured=True)[:6]
    serializer = ItemListSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def stats(request):
    total_items = Item.objects.filter(status='active').count()
    total_users = Item.objects.values('user').distinct().count()
    completed_deals = Item.objects.filter(status='sold').count()
    
    return Response({
        'total_items': total_items,
        'total_users': total_users,
        'completed_deals': completed_deals,
    })
